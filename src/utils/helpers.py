import random
import string


class Theme:
    BG_DARKEST    = "#0f0a00"
    BG_DARK       = "#181000"
    BG_CARD       = "#241a06"
    BG_INPUT      = "#1a1200"

    NEON_PRIMARY   = "#ff8c00"
    NEON_SECONDARY = "#ffcc00"
    NEON_ACCENT    = "#ffaa33"
    NEON_YELLOW    = "#ffe600"
    NEON_RED       = "#ff2040"

    TEXT_PRIMARY  = "#f0e0c0"
    TEXT_DIM      = "#6a5a3a"
    TEXT_LOG      = "#f0b860"

    BORDER_GLOW   = "#ff8c00"
    BORDER_DIM    = "#332200"

    BUTTON_FG     = "#0f0a00"
    BUTTON_HOVER  = "#ffcc00"

    PROGRESS_BG   = "#181000"

    GLOW_ALT      = "#cc7000"

    FONT_FAMILY   = "Consolas"
    CORNER_RADIUS = 14


def gen_hex_address() -> str:
    suffix = ''.join(random.choices("0123456789ABCDEF", k=8))
    return f"0x7FF8{suffix}"


def gen_license_key() -> str:
    parts = [
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        for _ in range(4)
    ]
    return '-'.join(parts)


def gen_sha256_fragment() -> str:
    return ''.join(random.choices("0123456789abcdef", k=16))


def gen_error_code() -> str:
    prefix = random.choice(["E_PATCH", "E_HOOK", "E_LICENSE", "E_AUTH", "E_SIGCHK"])
    num = random.randint(1000, 9999)
    return f"{prefix}_{num}"


def get_phase_logs() -> list[list[str]]:
    addr1, addr2, addr3 = gen_hex_address(), gen_hex_address(), gen_hex_address()
    addr4, addr5 = gen_hex_address(), gen_hex_address()
    key = gen_license_key()
    sha = gen_sha256_fragment()

    phase_scan = [
        f"[INIT]  Initializing MesBreak™ v5.0.1...",
        f"[INIT]  Target: Messari",
        f"[SCAN]  Enumerating process handles...",
        f"[SCAN]  Found target module at {addr1}",
        f"[SCAN]  Module hash: {sha}...",
        f"[SCAN]  Validating PE headers... OK",
    ]

    phase_patch = [
        f"[PATCH] Suspending watchdog thread at {addr2}",
        f"[PATCH] NOP-slide injected: {addr3} → {addr3}+0x40",
        f"[PATCH] Hooking license API at {addr4}",
        f"[PATCH] Overwriting subscription check → jmp 0x90909090",
        f"[PATCH] Bypassing certificate pinning...",
        f"[PATCH] Signature validation disabled at {addr5}",
    ]

    phase_activate = [
        f"[ACTIV] Generating license token: {key}",
        f"[ACTIV] Injecting feature flags...",
        f"[ACTIV] Telemetry hooks neutralized",
        f"[ACTIV] Rate limiter patched → unlimited",
        f"[ACTIV] Auth token refreshed",
    ]

    phase_verify = [
        f"[VERIF] Running integrity self-check... PASS",
        f"[VERIF] Anti-debug traps cleared",
        f"[VERIF] Memory region sealed: RWX → RX",
        f"[VERIF] Cleanup: removing staging artifacts",
    ]

    return [phase_scan, phase_patch, phase_activate, phase_verify]


def get_error_logs() -> list[str]:
    err = gen_error_code()
    addr = gen_hex_address()
    ver_expected = f"{random.randint(4, 6)}.{random.randint(0, 9)}.{random.randint(100, 999)}"
    ver_found = f"{random.randint(7, 12)}.{random.randint(0, 9)}.{random.randint(0, 99)}"
    sha = gen_sha256_fragment()

    return [
        f"[WARN]  Unexpected module version detected",
        f"[ERROR] Version mismatch: expected {ver_expected}, found {ver_found}",
        f"[ERROR] Signature verification FAILED at {addr}",
        f"[ERROR] Anti-tamper protection triggered — code {err}",
        f"[ERROR] License server returned HTTP 403 — token revoked",
        f"[ERROR] Checksum mismatch: {sha}... ≠ expected hash",
        f"[FATAL] Injection pipeline aborted — rollback initiated",
        f"[FATAL] Restoring original bytes at {gen_hex_address()}... OK",
        f"[FATAL] All patches reverted — target is unmodified",
    ]


def random_delay(min_s: float = 0.15, max_s: float = 0.65) -> float:
    return random.uniform(min_s, max_s)


FINAL_ERROR_BANNER = """
╔══════════════════════════════════════════════════════════╗
║            I N J E C T I O N   F A I L E D               ║
╠══════════════════════════════════════════════════════════╣
║  Status  :  ██ FATAL ERROR ██                            ║
║  Code    :  E_VERSION_MISMATCH / E_SIGFAIL               ║
║  Detail  :  Messari version is not supported             ║
║             MSR Crack v5.0 requires target ≤ 6.x          ║
║             Detected target version 11.2.x or newer      ║
║  Action  :  Update patcher or downgrade target app       ║
╚══════════════════════════════════════════════════════════╝
"""
