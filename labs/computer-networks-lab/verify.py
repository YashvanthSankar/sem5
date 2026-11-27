"""Small end-to-end checks for the exam servers; run with python3 verify.py."""

import contextlib
import pathlib
import socket
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).parent


@contextlib.contextmanager
def server(lab):
    with tempfile.TemporaryDirectory() as work:
        process = subprocess.Popen(
            [sys.executable, "-u", str(ROOT / f"lab{lab}" / "server.py")],
            cwd=work, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        try:
            for _ in range(50):
                if process.poll() is not None:
                    raise RuntimeError(process.stderr.read().decode())
                try:
                    probe = socket.create_connection(("127.0.0.1", 18080), timeout=0.2)
                    probe.close()
                    break
                except OSError:
                    time.sleep(0.1)
            else:
                raise RuntimeError(f"Lab {lab} server did not start")
            yield pathlib.Path(work)
        finally:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def connect(binary=False):
    sock = socket.create_connection(("127.0.0.1", 18080), timeout=3)
    sock.settimeout(3)
    return sock, sock.makefile("rb" if binary else "r")


def send(sock, line):
    sock.sendall((line + "\n").encode())


def line(reader):
    value = reader.readline()
    return value.decode().strip() if isinstance(value, bytes) else value.strip()


def check_lab2():
    with server(2):
        sock, _ = connect()
        sock.sendall(b"HeLLo")
        assert sock.recv(1024) == b"hello"
        sock.close()


def check_lab3():
    with server(3):
        a, ar = connect()
        b, br = connect()
        send(a, "cat")
        assert line(ar) == "cat"
        send(b, "cat")
        assert line(br) == "cat"
        send(b, "dog")
        assert line(br) == "cat,dog"
        send(a, "exit")
        send(b, "exit")
        a.close(); b.close()


def check_lab4():
    with server(4) as work:
        sock, reader = connect(True)
        send(sock, "NEW")
        name = line(reader)
        send(sock, "notes.txt")
        assert line(reader) == "READY"
        send(sock, "5")
        sock.sendall(b"hello")
        assert line(reader) == f"Upload Complete for {name}_notes.txt"
        sock.close()
        assert (work / "uploads" / f"{name}_notes.txt").read_bytes() == b"hello"
        sock, reader = connect(True)
        send(sock, name)
        assert line(reader) == name
        send(sock, "notes.txt")
        assert line(reader) == "File already exists"
        send(sock, "")
        sock.close()
        for filename, payload in [("essay.docx", b"DOCX"), ("paper.pdf", b"PDF"),
                                  ("clip.mp4", b"MP4")]:
            sock, reader = connect(True)
            send(sock, "NEW")
            user = line(reader)
            send(sock, filename)
            assert line(reader) == "READY"
            send(sock, str(len(payload)))
            sock.sendall(payload)
            assert line(reader) == f"Upload Complete for {user}_{filename}"
            sock.close()
            assert (work / "uploads" / f"{user}_{filename}").read_bytes() == payload


def check_lab5():
    with server(5) as work:
        a, ar = connect()
        b, br = connect()
        send(a, "alice"); assert line(ar).startswith("OK")
        send(b, "bob"); assert line(br).startswith("OK")
        c, cr = connect()
        send(c, "alice"); assert line(cr).startswith("TAKEN")
        send(c, "charlie"); assert line(cr).startswith("OK")
        send(a, "/users"); assert "bob" in line(ar)
        send(a, "bob:hello"); assert line(br) == "MSG alice: hello"
        send(a, "broadcast:all"); assert "alice: all" in line(br)
        send(a, "nobody:hi"); assert "User Not Online" in line(ar)
        send(a, "/exit"); send(b, "/exit"); send(c, "/exit")
        a.close(); b.close(); c.close()
        time.sleep(0.1)
        assert (work / "log.txt").exists()


def check_lab6():
    with server(6):
        a, ar = connect(True)
        b, br = connect(True)
        send(a, "alice"); assert line(ar).startswith("OK")
        send(b, "bob"); assert line(br).startswith("OK")
        send(a, "VIDEO alice bob 4 2 7 0.001 demo.mp4")
        a.sendall(b"ABCDEFG")
        assert line(br) == "VIDEO alice 4 2 7 demo.mp4"
        assert br.read(7) == b"ABCDEFG"
        assert "2/2" in line(ar)
        send(a, "VIDEO alice missing 4 1 4 0.001 other.mp4")
        a.sendall(b"TEST")
        assert "User Not Online" in line(ar)
        send(a, "/exit"); send(b, "/exit")
        a.close(); b.close()


def check_lab7():
    with server(7):
        a, ar = connect()
        b, br = connect()
        send(a, "NAME alice"); assert line(ar) == "OK alice"
        assert line(ar).startswith("WAIT")
        send(b, "NAME bob"); assert line(br) == "OK bob"
        assert line(ar) == "START bob"
        assert line(br) == "START alice"
        send(b, "CHAT hello")
        assert line(ar) == "CHAT bob: hello"
        send(a, "CHOICE rock")
        assert line(ar).startswith("WAIT")
        send(b, "CHOICE scissors")
        assert "alice wins" in line(ar)
        assert "alice wins" in line(br)
        c, cr = connect()
        send(c, "NAME alice")
        assert line(cr).startswith("TAKEN")
        send(c, "RANDOM")
        assert line(cr).startswith("OK player")
        assert line(cr).startswith("WAIT")
        send(a, "REPLAY")
        assert line(ar).startswith("START player")
        assert line(cr) == "START alice"
        send(a, "EXIT")
        assert "wins" in line(cr)
        send(b, "REPLAY")
        assert line(br).startswith("WAIT")
        send(b, "EXIT"); send(c, "EXIT")
        a.close(); b.close(); c.close()


def check_lab8():
    with server(8):
        sock, reader = connect()
        send(sock, "alice")
        assert line(reader).startswith("OK")
        head = line(reader)
        assert head == "QUESTIONS 5"
        for _ in range(5):
            assert len(line(reader).split("|")) == 5
        other, other_reader = connect()
        send(other, "alice")
        assert line(other_reader).startswith("TAKEN")
        send(other, "bob")
        assert line(other_reader).startswith("OK")
        assert line(other_reader) == "QUESTIONS 5"
        for _ in range(5): line(other_reader)
        send(sock, "ANSWERS B,C,C,B,B")
        assert line(reader).startswith("SCORE 5/5")
        send(sock, "REPLAY")
        assert line(reader) == "QUESTIONS 5"
        for _ in range(5): line(reader)
        send(sock, "ANSWERS -,-,-,-,-")
        assert line(reader).startswith("SCORE 0/5")
        send(sock, "EXIT")
        sock.close()
        send(other, "ANSWERS -,-,-,-,-")
        assert line(other_reader).startswith("SCORE 0/5")
        send(other, "EXIT")
        other.close()


def check_lab9():
    with server(9) as work:
        sock, reader = connect(True)
        send(sock, "LOGIN stud1 s123")
        assert line(reader).startswith("OK Student")
        send(sock, "LIST")
        files = line(reader)
        assert "academic/syllabus.txt" in files
        assert "administrative/" not in files
        send(sock, "READ administrative budget.txt")
        assert line(reader).startswith("DENIED")
        send(sock, "READ academic syllabus.txt")
        reply = line(reader)
        assert reply.startswith("OK ")
        assert b"syllabus" in reader.read(int(reply.split()[1]))
        send(sock, "UPLOAD academic new.txt 3")
        sock.sendall(b"abc")
        assert line(reader).startswith("DENIED")
        send(sock, "EXIT")
        sock.close()
        faculty, fr = connect(True)
        send(faculty, "LOGIN fac1 f123")
        assert line(fr).startswith("OK Faculty")
        send(faculty, "READ administrative budget.txt")
        reply = line(fr)
        assert reply.startswith("OK ")
        fr.read(int(reply.split()[1]))
        send(faculty, "UPLOAD academic notes.txt 4")
        faculty.sendall(b"note")
        assert line(fr).startswith("OK UPLOAD")
        send(faculty, "UPDATE administrative budget.txt 1")
        faculty.sendall(b"x")
        assert line(fr).startswith("DENIED")
        send(faculty, "EXIT")
        faculty.close()
        admin, ar = connect(True)
        send(admin, "LOGIN admin1 a123")
        assert line(ar).startswith("OK Administrator")
        send(admin, "UPDATE administrative budget.txt 3")
        admin.sendall(b"new")
        assert line(ar).startswith("OK UPDATE")
        send(admin, "EXIT")
        admin.close()
        assert (work / "server_files" / "administrative" / "budget.txt").read_bytes() == b"new"
        time.sleep(0.1)
        assert (work / "file_access_log.txt").exists()


if __name__ == "__main__":
    for lab in range(2, 10):
        globals()[f"check_lab{lab}"]()
        print(f"Lab {lab}: OK")
