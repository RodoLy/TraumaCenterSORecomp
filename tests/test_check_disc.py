"""Disc checker tests on a hand-built disc folder, so no game data is needed.

Pruebas del verificador de disco con una carpeta de disco hecha a mano, sin datos del juego.

Until a real disc is checked, the expected revision and SHA-1 are not recorded, so the checker
only compares the game ID and prints the other two values so they can be written down.

Hasta revisar un disco real, la revisión y el SHA-1 esperados no están registrados, así que el
verificador solo compara el ID del juego e imprime los otros dos valores para anotarlos.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import check_disc  # noqa: E402
from dol import write_dol  # noqa: E402
from ppc_encode import BLR  # noqa: E402

TEXT_ADDRESS = 0x80003100
DISC_HEADER_SIZE = 0x440  # boot.bin is the disc header


def make_disc(folder: Path, game_id: bytes, revision: int) -> Path:
    system = folder / "sys"
    system.mkdir(parents=True)
    header = bytearray(DISC_HEADER_SIZE)
    header[check_disc.GAME_ID_FIELD] = game_id
    header[check_disc.REVISION_OFFSET] = revision
    title = b"TRAUMA CENTER SECOND OPINION"
    header[check_disc.TITLE_FIELD.start : check_disc.TITLE_FIELD.start + len(title)] = title
    (system / "boot.bin").write_bytes(header)
    write_dol(system / "main.dol", text={0: (TEXT_ADDRESS, [BLR])}, data={}, entry=TEXT_ADDRESS)
    return folder


def run_checker(monkeypatch, disc: Path) -> int:
    monkeypatch.setattr(sys, "argv", ["check_disc.py", str(disc)])
    return check_disc.main()


def test_with_nothing_recorded_the_game_id_is_enough_and_the_values_to_record_are_printed(
    tmp_path, monkeypatch, capsys
):
    disc = make_disc(tmp_path / "disc", b"RKDEEB", 0)

    assert run_checker(monkeypatch, disc) == 0
    report = capsys.readouterr().out
    assert "Revision: 0  (not recorded yet" in report
    assert "write it as EXPECTED_DOL_SHA1" in report
    assert "Record the revision and the SHA-1 above" in report


def test_another_game_is_a_mismatch(tmp_path, monkeypatch, capsys):
    disc = make_disc(tmp_path / "disc", b"RBIEE9", 1)

    assert run_checker(monkeypatch, disc) == check_disc.EXIT_MISMATCH
    assert "MISMATCH" in capsys.readouterr().out


def test_once_recorded_a_different_main_dol_is_a_mismatch(tmp_path, monkeypatch, capsys):
    disc = make_disc(tmp_path / "disc", b"RKDEEB", 0)
    monkeypatch.setattr(check_disc, "EXPECTED_REVISION", 0)
    monkeypatch.setattr(check_disc, "EXPECTED_DOL_SHA1", "0" * 40)

    assert run_checker(monkeypatch, disc) == check_disc.EXIT_MISMATCH
    assert f"expected {'0' * 40}" in capsys.readouterr().out


def test_a_folder_without_sys_files_is_an_error(tmp_path, monkeypatch):
    with pytest.raises(SystemExit):
        run_checker(monkeypatch, tmp_path)
