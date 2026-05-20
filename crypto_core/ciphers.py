import math
from typing import Dict, List, Tuple, Any

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _char_index(ch: str) -> int:
    return ord(ch.upper()) - ord("A")


def _shift_char(ch: str, new_index: int) -> str:
    out = ALPHABET[new_index % 26]
    return out if ch.isupper() else out.lower()


def _mod_inverse(a: int, m: int = 26) -> int:
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Nilai {a} tidak memiliki invers modulo {m}.")


def _letters_only(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch.isalpha())


def caesar_cipher(text: str, shift: int, mode: str) -> Dict[str, Any]:
    if not 1 <= shift <= 25:
        raise ValueError("Shift Caesar harus berada pada rentang 1 sampai 25.")

    used_shift = shift if mode == "encrypt" else -shift
    output = []
    steps = [
        f"Rumus enkripsi: C = (P + k) mod 26.",
        f"Rumus dekripsi: P = (C - k) mod 26.",
        f"Shift yang digunakan: {shift}.",
    ]

    for ch in text:
        if ch.isalpha():
            old_index = _char_index(ch)
            new_index = (old_index + used_shift) % 26
            output.append(_shift_char(ch, new_index))
            if len(steps) < 80:
                symbol = "C" if mode == "encrypt" else "P"
                sign = "+" if mode == "encrypt" else "-"
                steps.append(
                    f"{ch} = {old_index}; {symbol} = ({old_index} {sign} {shift}) mod 26 = {new_index}; hasil = {_shift_char(ch, new_index)}."
                )
        else:
            output.append(ch)
            if len(steps) < 80:
                steps.append(f"Karakter non-huruf '{ch}' tidak diubah.")

    return {
        "result": "".join(output),
        "steps": steps,
        "meta": {"formula": "C=(P+k) mod 26 / P=(C-k) mod 26"},
    }


def vigenere_cipher(text: str, keyword: str, mode: str) -> Dict[str, Any]:
    keyword = keyword.strip()
    if not keyword or not keyword.isalpha():
        raise ValueError("Keyword Vigenère harus berisi huruf saja.")

    keys = [_char_index(ch) for ch in keyword.upper()]
    output = []
    key_pos = 0
    steps = [
        "Rumus enkripsi: C = (P + K) mod 26.",
        "Rumus dekripsi: P = (C - K) mod 26.",
        f"Keyword: {keyword.upper()} dengan nilai {keys}.",
    ]

    for ch in text:
        if ch.isalpha():
            p = _char_index(ch)
            k = keys[key_pos % len(keys)]
            new_index = (p + k) % 26 if mode == "encrypt" else (p - k) % 26
            output.append(_shift_char(ch, new_index))
            if len(steps) < 100:
                symbol = "C" if mode == "encrypt" else "P"
                sign = "+" if mode == "encrypt" else "-"
                steps.append(
                    f"{ch} memakai key {ALPHABET[k]}={k}; {symbol}=({p} {sign} {k}) mod 26 = {new_index}; hasil = {_shift_char(ch, new_index)}."
                )
            key_pos += 1
        else:
            output.append(ch)
            if len(steps) < 100:
                steps.append(f"Karakter non-huruf '{ch}' dilewati dan tidak memakai key.")

    return {
        "result": "".join(output),
        "steps": steps,
        "meta": {"keyword": keyword.upper()},
    }


def affine_cipher(text: str, a: int, b: int, mode: str) -> Dict[str, Any]:
    if math.gcd(a, 26) != 1:
        raise ValueError("Nilai a harus relatif prima dengan 26. Contoh yang valid: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25.")
    b %= 26
    inv_a = _mod_inverse(a, 26)
    output = []
    steps = [
        "Rumus enkripsi: C = (aP + b) mod 26.",
        "Rumus dekripsi: P = a⁻¹(C - b) mod 26.",
        f"a = {a}, b = {b}, invers a modulo 26 = {inv_a}.",
    ]

    for ch in text:
        if ch.isalpha():
            x = _char_index(ch)
            if mode == "encrypt":
                new_index = (a * x + b) % 26
                detail = f"C = ({a} × {x} + {b}) mod 26 = {new_index}"
            else:
                new_index = (inv_a * (x - b)) % 26
                detail = f"P = {inv_a} × ({x} - {b}) mod 26 = {new_index}"
            output.append(_shift_char(ch, new_index))
            if len(steps) < 100:
                steps.append(f"{ch}={x}; {detail}; hasil = {_shift_char(ch, new_index)}.")
        else:
            output.append(ch)
            if len(steps) < 100:
                steps.append(f"Karakter non-huruf '{ch}' tidak diubah.")

    return {
        "result": "".join(output),
        "steps": steps,
        "meta": {"a": a, "b": b, "inverse_a": inv_a},
    }


def _parse_matrix(raw: str) -> List[List[int]]:
    cleaned = raw.replace(";", "\n")
    rows = []
    for row in cleaned.splitlines():
        row = row.strip()
        if not row:
            continue
        parts = row.replace(",", " ").split()
        rows.append([int(x) % 26 for x in parts])

    if len(rows) not in (2, 3):
        raise ValueError("Matriks Hill harus berukuran 2x2 atau 3x3.")
    n = len(rows)
    if any(len(row) != n for row in rows):
        raise ValueError("Jumlah kolom matriks harus sama dengan jumlah baris, yaitu 2x2 atau 3x3.")
    det = _determinant(rows) % 26
    if math.gcd(det, 26) != 1:
        raise ValueError(f"Determinan matriks = {det}. Matriks tidak invertible modulo 26, jadi tidak bisa dipakai untuk Hill Cipher.")
    return rows


def _determinant(matrix: List[List[int]]) -> int:
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col + 1:] for row in matrix[1:]]
        det += ((-1) ** col) * matrix[0][col] * _determinant(minor)
    return det


def _matrix_inverse_mod(matrix: List[List[int]], mod: int = 26) -> List[List[int]]:
    n = len(matrix)
    det = _determinant(matrix)
    det_mod = det % mod
    det_inv = _mod_inverse(det_mod, mod)

    if n == 2:
        a, b = matrix[0]
        c, d = matrix[1]
        adj = [[d, -b], [-c, a]]
    else:
        cofactors = []
        for r in range(n):
            cofactor_row = []
            for c in range(n):
                minor = [row[:c] + row[c + 1:] for i, row in enumerate(matrix) if i != r]
                cofactor_row.append(((-1) ** (r + c)) * _determinant(minor))
            cofactors.append(cofactor_row)
        adj = [[cofactors[c][r] for c in range(n)] for r in range(n)]

    return [[(det_inv * adj[r][c]) % mod for c in range(n)] for r in range(n)]


def _matrix_vector_mul(matrix: List[List[int]], vector: List[int], mod: int = 26) -> List[int]:
    result = []
    for row in matrix:
        result.append(sum(row[i] * vector[i] for i in range(len(vector))) % mod)
    return result


def hill_cipher(text: str, raw_matrix: str, mode: str) -> Dict[str, Any]:
    key_matrix = _parse_matrix(raw_matrix)
    working_matrix = key_matrix if mode == "encrypt" else _matrix_inverse_mod(key_matrix, 26)
    n = len(key_matrix)
    normalized = _letters_only(text)
    if not normalized:
        raise ValueError("Teks Hill Cipher harus memiliki minimal satu huruf.")
    padding = (n - len(normalized) % n) % n
    normalized_padded = normalized + ("X" * padding)

    steps = [
        "Hill Cipher memakai angka A=0 sampai Z=25.",
        "Rumus enkripsi: C = K × P mod 26.",
        "Rumus dekripsi: P = K⁻¹ × C mod 26.",
        f"Matriks kunci K = {key_matrix}.",
        f"Determinan K mod 26 = {_determinant(key_matrix) % 26}.",
    ]
    if mode == "decrypt":
        steps.append(f"Matriks invers K⁻¹ mod 26 = {working_matrix}.")
    if padding:
        steps.append(f"Teks dinormalisasi menjadi {normalized_padded}. Tambahan padding: {'X' * padding}.")
    else:
        steps.append(f"Teks dinormalisasi menjadi {normalized_padded}. Tidak perlu padding.")

    result_letters = []
    block_steps = []
    for i in range(0, len(normalized_padded), n):
        block = normalized_padded[i:i + n]
        vector = [_char_index(ch) for ch in block]
        output_vector = _matrix_vector_mul(working_matrix, vector, 26)
        output_block = "".join(ALPHABET[x] for x in output_vector)
        result_letters.append(output_block)
        calc_rows = []
        for row in working_matrix:
            raw_sum = " + ".join(f"{row[j]}×{vector[j]}" for j in range(n))
            calc_rows.append(f"({raw_sum}) mod 26")
        block_steps.append({
            "block": block,
            "vector": vector,
            "calculation": calc_rows,
            "output_vector": output_vector,
            "output_block": output_block,
        })
        if len(steps) < 80:
            steps.append(f"Blok {block} -> {vector}; hasil perkalian = {output_vector}; huruf = {output_block}.")

    return {
        "result": "".join(result_letters),
        "steps": steps,
        "meta": {
            "matrix": key_matrix,
            "working_matrix": working_matrix,
            "normalized_text": normalized_padded,
            "blocks": block_steps,
        },
    }


def _playfair_matrix(keyword: str) -> List[List[str]]:
    keyword = keyword.upper().replace("J", "I")
    seen = set()
    letters = []
    for ch in keyword + ALPHABET:
        if ch == "J":
            continue
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            letters.append(ch)
    return [letters[i:i + 5] for i in range(0, 25, 5)]


def _playfair_positions(matrix: List[List[str]]) -> Dict[str, Tuple[int, int]]:
    return {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}


def _playfair_pairs(text: str) -> List[str]:
    letters = _letters_only(text).replace("J", "I")
    pairs = []
    i = 0
    while i < len(letters):
        a = letters[i]
        b = letters[i + 1] if i + 1 < len(letters) else "X"
        if a == b:
            pairs.append(a + "X")
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    if pairs and len(pairs[-1]) == 1:
        pairs[-1] += "X"
    return pairs


def playfair_cipher(text: str, keyword: str, mode: str) -> Dict[str, Any]:
    keyword = keyword.strip()
    if not keyword or not keyword.replace(" ", "").isalpha():
        raise ValueError("Keyword Playfair harus berisi huruf.")
    matrix = _playfair_matrix(keyword)
    pos = _playfair_positions(matrix)

    if mode == "encrypt":
        pairs = _playfair_pairs(text)
    else:
        normalized = _letters_only(text).replace("J", "I")
        if len(normalized) % 2 != 0:
            normalized += "X"
        pairs = [normalized[i:i + 2] for i in range(0, len(normalized), 2)]

    if not pairs:
        raise ValueError("Teks Playfair harus memiliki minimal satu huruf.")

    steps = [
        "Playfair memakai matriks 5x5. Huruf J digabung dengan I.",
        "Aturan: satu baris geser kanan/kiri, satu kolom geser bawah/atas, beda baris dan kolom ambil sudut persegi.",
        f"Keyword: {keyword.upper().replace('J', 'I')}.",
        f"Pairing huruf: {', '.join(pairs)}.",
    ]

    result = []
    pair_steps = []
    for pair in pairs:
        a, b = pair[0], pair[1]
        ra, ca = pos[a]
        rb, cb = pos[b]
        if ra == rb:
            if mode == "encrypt":
                out_a = matrix[ra][(ca + 1) % 5]
                out_b = matrix[rb][(cb + 1) % 5]
                rule = "Satu baris: geser masing-masing huruf ke kanan."
            else:
                out_a = matrix[ra][(ca - 1) % 5]
                out_b = matrix[rb][(cb - 1) % 5]
                rule = "Satu baris: geser masing-masing huruf ke kiri."
        elif ca == cb:
            if mode == "encrypt":
                out_a = matrix[(ra + 1) % 5][ca]
                out_b = matrix[(rb + 1) % 5][cb]
                rule = "Satu kolom: geser masing-masing huruf ke bawah."
            else:
                out_a = matrix[(ra - 1) % 5][ca]
                out_b = matrix[(rb - 1) % 5][cb]
                rule = "Satu kolom: geser masing-masing huruf ke atas."
        else:
            out_a = matrix[ra][cb]
            out_b = matrix[rb][ca]
            rule = "Beda baris dan kolom: ambil huruf pada sudut persegi yang sejajar."
        out_pair = out_a + out_b
        result.append(out_pair)
        pair_steps.append({"pair": pair, "positions": [(ra, ca), (rb, cb)], "rule": rule, "output": out_pair})
        if len(steps) < 100:
            steps.append(f"Pair {pair}: posisi {a}=({ra+1},{ca+1}), {b}=({rb+1},{cb+1}). {rule} Hasil = {out_pair}.")

    return {
        "result": "".join(result),
        "steps": steps,
        "meta": {"matrix": matrix, "pairs": pair_steps},
    }


def run_cipher(algorithm: str, mode: str, text: str, form: Dict[str, str]) -> Dict[str, Any]:
    if mode not in {"encrypt", "decrypt"}:
        raise ValueError("Mode harus enkripsi atau dekripsi.")
    if not text:
        raise ValueError("Teks tidak boleh kosong.")

    if algorithm == "caesar":
        return caesar_cipher(text, int(form.get("caesar_shift", "0")), mode)
    if algorithm == "vigenere":
        return vigenere_cipher(text, form.get("vigenere_key", ""), mode)
    if algorithm == "affine":
        return affine_cipher(text, int(form.get("affine_a", "0")), int(form.get("affine_b", "0")), mode)
    if algorithm == "hill":
        return hill_cipher(text, form.get("hill_matrix", ""), mode)
    if algorithm == "playfair":
        return playfair_cipher(text, form.get("playfair_key", ""), mode)

    raise ValueError("Algoritma tidak dikenal.")
