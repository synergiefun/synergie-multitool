
# ================================================================
#  SYNERGIE OSINT CLI V3.0 | PREMIUM EDITION
# ================================================================

import os
import random
import secrets
import string
import shutil
import base64
import ast
import operator
import re
import sys
import json
import time
import socket
import hashlib
import platform
import subprocess
import webbrowser
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.align import Align
    from rich import box
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Installe les dépendances avec : py -m pip install rich dnspython phonenumbers")
    sys.exit(1)

try:
    import dns.resolver
except ImportError:
    dns = None

APP_NAME = "SYNERGIE MULTITOOL"
VERSION = "6.1 FINAL"
ROOT = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)
console = Console()

LOGO = r"""
 ███████╗██╗   ██╗███╗   ██╗███████╗██████╗  ██████╗ ██╗███████╗
 ██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝██╔══██╗██╔════╝ ██║██╔════╝
 ███████╗ ╚████╔╝ ██╔██╗ ██║█████╗  ██████╔╝██║  ███╗██║█████╗
 ╚════██║  ╚██╔╝  ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██║██╔══╝
 ███████║   ██║   ██║ ╚████║███████╗██║  ██║╚██████╔╝██║██║
 ╚══════╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝
"""

def clear():
    """Efface l'écran visible du terminal avant d'afficher une nouvelle page.

    Le lancement de cls/clear aide aussi dans certains terminaux Windows où
    console.clear() seul ne rafraîchit pas correctement l'affichage.
    """
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        pass
    try:
        console.clear(home=True)
    except Exception:
        # Repli ANSI pour les terminaux compatibles.
        print("\033[2J\033[H", end="", flush=True)

def wait():
    console.input("\n[bold bright_cyan] › [/bold bright_cyan][grey70]Entrée pour continuer...[/grey70]")

def ask(message, default=""):
    return Prompt.ask(f"[bold bright_cyan] › {message}[/bold bright_cyan]", default=default).strip()

def confirm(message, default=False):
    return Confirm.ask(f"[bold bright_cyan] › {message}[/bold bright_cyan]", default=default)

def title(name, subtitle=""):
    clear()
    content = Text(name.upper(), style="bold bright_cyan", justify="center")
    if subtitle:
        content.append("\n" + subtitle, style="grey62")
    console.print(Panel(Align.center(content), border_style="bright_cyan", box=box.DOUBLE, padding=(1, 2)))

def status(message, kind="info"):
    styles = {
        "ok": ("✓", "bright_green"),
        "warn": ("!", "bright_yellow"),
        "error": ("✗", "bright_red"),
        "info": ("›", "bright_cyan"),
    }
    symbol, color = styles.get(kind, styles["info"])
    console.print(f" [{color}]{symbol}[/{color}] {message}")

def make_table(name, columns):
    table = Table(title=name, box=box.ROUNDED, border_style="bright_cyan", header_style="bold bright_cyan", expand=True)
    for col in columns:
        table.add_column(col)
    return table

def save_report(name, data):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    path = REPORTS_DIR / f"{stamp}_{safe_name}.json"
    report = {
        "application": APP_NAME,
        "version": VERSION,
        "created_at": datetime.now().astimezone().isoformat(),
        "type": name,
        "data": data,
    }
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    status(f"Rapport sauvegardé : [white]{path.name}[/white]", "ok")

def maybe_save(name, data):
    if confirm("Enregistrer les résultats en JSON ?", default=False):
        save_report(name, data)

def open_link(url):
    console.print(f"\n[bright_cyan underline]{url}[/bright_cyan underline]")
    if confirm("Ouvrir dans le navigateur ?", default=True):
        webbrowser.open(url)

def valid_discord_id(value):
    return value.isdigit() and 17 <= len(value) <= 20


# ---------------- ANIMATION DE DÉMARRAGE ----------------

def rainbow_text(value):
    palette = ["bright_green", "bright_cyan", "bright_blue", "bright_magenta", "bright_red", "bright_yellow"]
    result = Text()
    for i, char in enumerate(value):
        result.append(char, style=f"bold {palette[i % len(palette)]}")
    return result

def startup_animation():
    """Animation de démarrage en chiffres binaires, sans caractères exotiques."""
    from rich.live import Live
    from rich.align import Align
    width = min(max(shutil.get_terminal_size((100, 30)).columns - 12, 24), 80)
    height = 10
    cols = max(12, width // 2)
    drops = [random.randrange(-height, 0) for _ in range(cols)]
    clear()
    console.print(Align.center(rainbow_text("SYNERGIE")))
    console.print(Align.center("[bold white]MULTITOOL • INITIALISATION SÉCURISÉE[/bold white]"))
    with Live(console=console, refresh_per_second=20, screen=False) as live:
        for frame in range(28):
            rows = []
            for y in range(height):
                line = Text()
                for x in range(cols):
                    ch = " "
                    if drops[x] == y or drops[x] - 1 == y:
                        ch = random.choice("01")
                    if ch == " ":
                        line.append(" ")
                    else:
                        line.append(ch, style=random.choice(["bright_green", "green", "dark_green", "bright_cyan"]))
                rows.append(line)
            for x in range(cols):
                drops[x] += 1
                if drops[x] > height + random.randint(0, 5):
                    drops[x] = random.randint(-height, -1)
            body = Text()
            for line in rows:
                body.append_text(line)
                body.append("\n")
            pct = min(100, int((frame + 1) / 28 * 100))
            bar_width = 32
            filled = int(bar_width * pct / 100)
            bar = Text("[" + "█" * filled + "░" * (bar_width - filled) + f"] {pct:3d}%", style="bold bright_cyan")
            panel = Panel(
                Align.center(Group(body, Text("CHARGEMENT DES MODULES", style="bold bright_green"), Align.center(bar))),
                title="[bold bright_cyan]SYNERGIE BOOT SEQUENCE[/bold bright_cyan]",
                border_style="bright_green",
                box=box.DOUBLE,
                padding=(1, 2),
            )
            live.update(Align.center(panel))
            time.sleep(0.045)
    clear()



def big_synergie_logo():
    """Logo SYNERGIE en grandes lettres ASCII, avec le E à trois barres."""
    patterns = {
        "S": ["█████", "█    ", "█    ", "█████", "    █", "    █", "█████"],
        "Y": ["█   █", "█   █", " █ █ ", "  █  ", "  █  ", "  █  ", "  █  "],
        "N": ["█   █", "██  █", "██  █", "█ █ █", "█  ██", "█  ██", "█   █"],
        "E": ["█████", "█    ", "█    ", "████ ", "█    ", "█    ", "█████"],
        "R": ["████ ", "█   █", "█   █", "████ ", "█ █  ", "█  █ ", "█   █"],
        "G": ["█████", "█    ", "█    ", "█ ███", "█   █", "█   █", "█████"],
        "I": ["█████", "  █  ", "  █  ", "  █  ", "  █  ", "  █  ", "█████"],
    }
    letters = list("SYNERGIE")
    palette = ["bright_green", "bright_cyan", "bright_blue", "bright_magenta",
               "bright_red", "bright_yellow", "bright_green", "bright_cyan"]
    rows = []
    for row_index in range(7):
        line = Text(justify="center")
        for letter_index, letter in enumerate(letters):
            line.append(patterns[letter][row_index], style=f"bold {palette[letter_index]}")
            if letter_index < len(letters) - 1:
                line.append("  ")
        rows.append(line)
    return Group(*rows)


# ---------------- LOGO HISTORIQUE MULTICOLORE ----------------

def legacy_logo_multicolor():
    """Rend le logo ASCII historique en grand, avec un dégradé multicolore."""
    palette = ["bright_cyan", "bright_blue", "bright_magenta", "bright_red", "bright_yellow", "bright_green"]
    rows = []
    for row in LOGO.strip("\n").splitlines():
        line = Text(justify="center")
        for index, char in enumerate(row.rstrip()):
            if char.isspace():
                line.append(char)
            else:
                line.append(char, style=f"bold {palette[(index // 3) % len(palette)]}")
        rows.append(line)
    return Group(*rows)


# ---------------- DASHBOARD ----------------

def dashboard():
    clear()
    from rich.align import Align

    # Logo historique d'origine : grand, centré et multicolore.
    console.print(Align.center(legacy_logo_multicolor()))
    console.print(Align.center(Text("M U L T I T O O L  •  É D I T I O N  F I N A L E", style="bold white")))
    console.print(Align.center(Text("OSINT PUBLIC • DISCORD • TÉLÉPHONE • RÉSEAU • SYSTÈME • UTILITAIRES", style="bright_cyan")))
    console.print()

    files = list(REPORTS_DIR.glob("*.json"))
    stats = Table.grid(expand=True, padding=(0, 2))
    stats.add_column(justify="center")
    stats.add_column(justify="center")
    stats.add_column(justify="center")
    stats.add_row(
        f"[bold bright_magenta]{len(files)}[/bold bright_magenta]\n[grey62]RAPPORTS[/grey62]",
        f"[bold bright_green]{platform.system()}[/bold bright_green]\n[grey62]SYSTÈME[/grey62]",
        f"[bold bright_cyan]V{VERSION}[/bold bright_cyan]\n[grey62]VERSION[/grey62]",
    )
    console.print(Panel(stats, title="[bold white]◈ VUE DU SYSTÈME[/bold white]", border_style="bright_cyan", box=box.ROUNDED))
    console.print()

def show_menu(name, items, border="bright_cyan"):
    table = Table(box=box.ROUNDED, border_style=border, show_header=False, expand=True, padding=(0, 1))
    table.add_column("N°", style="bold bright_cyan", width=5)
    table.add_column("Fonction", style="white")
    for number, label in items:
        table.add_row(number, label)
    console.print(Panel(table, title=f"[bold white]{name}[/bold white]", border_style=border, box=box.ROUNDED))

# ---------------- OSINT ----------------

def username_search():
    title("Username Intelligence", "Recherche de pseudos dans les sources publiques")
    username = ask("Pseudo")
    if not username:
        wait()
        return
    q = urllib.parse.quote_plus(username)
    links = {
        "Google": f"https://www.google.com/search?q={q}",
        "Bing": f"https://www.bing.com/search?q={q}",
        "DuckDuckGo": f"https://duckduckgo.com/?q={q}",
        "GitHub": f"https://github.com/search?q={q}",
        "Reddit": f"https://www.reddit.com/search/?q={q}",
        "YouTube": f"https://www.youtube.com/results?search_query={q}",
        "TikTok": f"https://www.tiktok.com/search?q={q}",
        "X": f"https://x.com/search?q={q}",
        "Instagram": f"https://www.google.com/search?q=site%3Ainstagram.com+{q}",
    }
    table = make_table("PUBLIC SEARCH", ["Source", "URL"])
    for name, url in links.items():
        table.add_row(name, url)
    console.print(table)
    maybe_save("username_search", {"username": username, "links": links})
    if confirm("Ouvrir toutes les recherches ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()

def name_search():
    title("Name Intelligence", "Recherche publique par nom ou prénom")
    name = ask("Nom ou prénom")
    if not name:
        wait()
        return
    q = urllib.parse.quote_plus(f'"{name}"')
    links = {
        "Google": f"https://www.google.com/search?q={q}",
        "Bing": f"https://www.bing.com/search?q={q}",
        "DuckDuckGo": f"https://duckduckgo.com/?q={q}",
        "LinkedIn": f"https://www.google.com/search?q=site%3Alinkedin.com+{q}",
        "GitHub": f"https://github.com/search?q={urllib.parse.quote_plus(name)}",
        "Reddit": f"https://www.reddit.com/search/?q={urllib.parse.quote_plus(name)}",
    }
    table = make_table("PUBLIC SEARCH", ["Source", "URL"])
    for site, url in links.items():
        table.add_row(site, url)
    console.print(table)
    maybe_save("name_search", {"query": name, "links": links})
    if confirm("Ouvrir les recherches ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()

def email_osint():
    title("Email Inspector", "Syntaxe et domaine")
    email = ask("Adresse e-mail")
    valid = bool(re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email))
    data = {"email": email, "syntax_valid": valid}
    table = make_table("EMAIL ANALYSIS", ["Champ", "Résultat"])
    table.add_row("Adresse", email or "(vide)")
    table.add_row("Syntaxe", "Valide" if valid else "Invalide")
    if valid:
        domain = email.rsplit("@", 1)[1]
        data["domain"] = domain
        table.add_row("Domaine", domain)
        if dns:
            try:
                mx = [str(a.exchange).rstrip(".") for a in dns.resolver.resolve(domain, "MX")]
                data["mx"] = mx
                table.add_row("MX", "\n".join(mx) or "Aucun")
            except Exception:
                data["mx"] = []
                table.add_row("MX", "Indisponible")
        else:
            table.add_row("MX", "Installe dnspython")
        data["public_search"] = "https://www.google.com/search?q=" + urllib.parse.quote_plus(f'"{email}"')
    console.print(table)
    if valid:
        open_link(data["public_search"])
    maybe_save("email_analysis", data)
    wait()

def tiktok_search():
    title("TikTok Search", "Recherche publique")
    query = ask("Pseudo ou mots-clés")
    if query:
        url = "https://www.tiktok.com/search?q=" + urllib.parse.quote_plus(query)
        open_link(url)
        maybe_save("tiktok_search", {"query": query, "url": url})
    wait()


# ---------------- OSINT SUPPLÉMENTAIRE (SOURCES PUBLIQUES) ----------------

def domain_osint():
    title("Domain Footprint", "Sources publiques et DNS — aucun scan intrusif")
    raw = ask("Domaine (ex. exemple.fr)")
    if not raw:
        wait()
        return
    parsed = urllib.parse.urlparse(raw if "://" in raw else "https://" + raw)
    domain = (parsed.hostname or "").strip(".").lower()
    if not domain or "." not in domain or any(c.isspace() for c in domain):
        status("Domaine invalide.", "error")
        wait()
        return
    data = {"domain": domain, "dns": {}, "public_sources": {}}
    table = make_table("DOMAIN FOOTPRINT", ["Élément", "Résultat"])
    table.add_row("Domaine normalisé", domain)
    if dns:
        for record_type in ("A", "AAAA", "MX", "NS", "TXT"):
            try:
                answers = [str(r).rstrip(".") for r in dns.resolver.resolve(domain, record_type, lifetime=3)]
                data["dns"][record_type] = answers
                table.add_row(f"DNS {record_type}", "\n".join(answers[:8]) or "Aucun")
            except Exception:
                data["dns"][record_type] = []
                table.add_row(f"DNS {record_type}", "Aucun résultat / non disponible")
    else:
        table.add_row("DNS", "Installe dnspython pour activer les requêtes DNS")
    encoded = urllib.parse.quote_plus(domain)
    links = {
        "Recherche web": f"https://www.google.com/search?q={encoded}",
        "Sous-domaines publics (crt.sh)": f"https://crt.sh/?q=%25.{urllib.parse.quote(domain, safe='')}",
        "RDAP / enregistrement": f"https://rdap.org/domain/{urllib.parse.quote(domain, safe='')}",
        "URLScan (recherche)": f"https://urlscan.io/search/#domain:{urllib.parse.quote(domain, safe='')}",
    }
    data["public_sources"] = links
    for label, url in links.items():
        table.add_row(label, url)
    console.print(table)
    console.print("[grey70]Les résultats DNS et les bases publiques peuvent être incomplets ou anciens.[/grey70]")
    maybe_save("domain_footprint", data)
    if confirm("Ouvrir les sources publiques dans le navigateur ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()


def username_deep_search():
    title("Username Footprint", "Recherche d'un pseudo sur plusieurs plateformes publiques")
    username = ask("Pseudo (sans @ si possible)")
    if not username:
        wait()
        return
    q = urllib.parse.quote_plus(username)
    links = {
        "Google exact": f"https://www.google.com/search?q={urllib.parse.quote_plus(chr(34) + username + chr(34))}",
        "GitHub": f"https://github.com/search?q={q}&type=users",
        "GitLab": f"https://gitlab.com/search?search={q}",
        "Reddit": f"https://www.reddit.com/search/?q={q}",
        "YouTube": f"https://www.youtube.com/results?search_query={q}",
        "Twitch": f"https://www.google.com/search?q=site%3Atwitch.tv+{q}",
        "Steam": f"https://steamcommunity.com/search/users/#text={urllib.parse.quote(username)}",
        "Pinterest": f"https://www.pinterest.com/search/users/?q={q}",
        "Medium": f"https://medium.com/search?q={q}",
        "Mastodon (recherche web)": f"https://www.google.com/search?q=site%3Amastodon.social+{q}",
        "X": f"https://x.com/search?q={q}",
        "TikTok": f"https://www.tiktok.com/search?q={q}",
    }
    table = make_table("PSEUDO — SOURCES PUBLIQUES", ["Plateforme", "Lien"])
    for label, url in links.items():
        table.add_row(label, url)
    console.print(table)
    console.print("[yellow]Un même pseudo ne prouve pas que les comptes appartiennent à la même personne.[/yellow]")
    maybe_save("username_deep_search", {"username": username, "links": links})
    if confirm("Ouvrir toutes les recherches ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()


def url_reputation_lookup():
    title("URL Reputation", "Préparer des vérifications publiques sans visiter la cible directement")
    raw = ask("URL ou domaine à vérifier")
    if not raw:
        wait()
        return
    parsed = urllib.parse.urlparse(raw if "://" in raw else "https://" + raw)
    host = parsed.hostname
    if not host:
        status("URL ou domaine invalide.", "error")
        wait()
        return
    value = parsed.geturl()
    q = urllib.parse.quote(value, safe="")
    domain_q = urllib.parse.quote(host, safe="")
    links = {
        "VirusTotal (recherche)": f"https://www.virustotal.com/gui/search/{q}",
        "URLScan (recherche)": f"https://urlscan.io/search/#domain:{domain_q}",
        "Google Safe Browsing (infos)": "https://transparencyreport.google.com/safe-browsing/search",
        "Recherche de signalements": f"https://www.google.com/search?q={urllib.parse.quote_plus(chr(34) + host + chr(34) + ' phishing OR malware OR scam')}",
    }
    table = make_table("SOURCES DE RÉPUTATION", ["Source", "Lien"])
    for label, url in links.items():
        table.add_row(label, url)
    console.print(table)
    console.print("[yellow]SYNERGIE ne déclare pas automatiquement une URL sûre ou dangereuse. Vérifie les résultats et évite d'ouvrir une URL suspecte.[/yellow]")
    maybe_save("url_reputation_links", {"url": value, "links": links})
    if confirm("Ouvrir les sources ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()


def public_query_builder():
    title("Public Search Builder", "Construire une recherche web ciblée et raisonnable")
    query = ask("Mots-clés")
    if not query:
        wait()
        return
    site = ask("Limiter à un domaine (facultatif, ex. github.com)")
    exact = ask("Expression exacte entre guillemets (facultatif)")
    filetype = ask("Type de document public (facultatif : pdf, docx, csv)")
    parts = []
    if exact:
        parts.append('"' + exact.replace('"', "") + '"')
    parts.append(query)
    if site:
        safe_site = re.sub(r"[^A-Za-z0-9._-]", "", site)
        if safe_site:
            parts.append("site:" + safe_site)
    if filetype:
        safe_type = re.sub(r"[^A-Za-z0-9]", "", filetype.lower())
        if safe_type:
            parts.append("filetype:" + safe_type)
    final_query = " ".join(parts)
    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(final_query)
    console.print(Panel(f"[bold bright_cyan]{final_query}[/bold bright_cyan]\n\n{url}", title="REQUÊTE CONSTRUITE", border_style="bright_cyan"))
    console.print("[grey70]À utiliser sur des informations publiques et dans le respect des autorisations et de la vie privée.[/grey70]")
    maybe_save("public_query_builder", {"query": final_query, "url": url})
    if confirm("Ouvrir la recherche ?"):
        webbrowser.open(url)
    wait()


def email_exposure_resources():
    title("Email Exposure Check", "Ressources publiques pour vérifier sa propre adresse")
    email = ask("Adresse e-mail à examiner")
    if not email:
        wait()
        return
    if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email):
        status("Format d'adresse e-mail invalide.", "error")
        wait()
        return
    domain = email.rsplit("@", 1)[1]
    links = {
        "Have I Been Pwned (vérification manuelle)": "https://haveibeenpwned.com/",
        "Recherche web exacte": "https://www.google.com/search?q=" + urllib.parse.quote_plus('"' + email + '"'),
        "Recherche du domaine": "https://www.google.com/search?q=" + urllib.parse.quote_plus(domain),
        "Conseils de sécurité Google": "https://safety.google/security/security-tips/",
    }
    table = make_table("RESSOURCES DE VÉRIFICATION", ["Ressource", "Lien"])
    for label, url in links.items():
        table.add_row(label, url)
    console.print(table)
    console.print("[yellow]Aucune base de fuites n'est interrogée automatiquement. Vérifie uniquement une adresse que tu es autorisé à contrôler. Les résultats publics ne prouvent pas l'absence de fuite.[/yellow]")
    maybe_save("email_exposure_resources", {"email": email, "domain": domain, "links": links})
    if confirm("Ouvrir les ressources ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()


def reverse_image_search():
    title("Reverse Image Search", "Recherche inversée à effectuer manuellement")
    console.print("1. Prépare une image que tu as le droit d'utiliser.")
    console.print("2. Ouvre l'un des moteurs, puis choisis l'option de recherche par image.")
    links = {
        "Google Lens": "https://lens.google.com/",
        "Bing Visual Search": "https://www.bing.com/visualsearch",
        "TinEye": "https://tineye.com/",
    }
    table = make_table("MOTEURS DE RECHERCHE D'IMAGES", ["Moteur", "Lien"])
    for label, url in links.items():
        table.add_row(label, url)
    console.print(table)
    console.print("[grey70]SYNERGIE n'envoie pas ton image : tu choisis toi-même si tu la téléverses sur un service externe.[/grey70]")
    if confirm("Ouvrir les moteurs dans le navigateur ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()


def public_social_search():
    title("Public Social Search", "Rechercher une expression dans des contenus publics")
    query = ask("Mot-clé, organisation ou expression publique")
    if not query:
        wait()
        return
    q = urllib.parse.quote_plus(query)
    links = {
        "Google": f"https://www.google.com/search?q={q}",
        "Bing": f"https://www.bing.com/search?q={q}",
        "Reddit": f"https://www.reddit.com/search/?q={q}",
        "YouTube": f"https://www.youtube.com/results?search_query={q}",
        "GitHub": f"https://github.com/search?q={q}",
        "Mastodon (web)": f"https://www.google.com/search?q=site%3Amastodon.social+{q}",
        "Actualités": f"https://news.google.com/search?q={q}",
    }
    table = make_table("RECHERCHE PUBLIQUE", ["Source", "Lien"])
    for label, url in links.items():
        table.add_row(label, url)
    console.print(table)
    maybe_save("public_social_search", {"query": query, "links": links})
    if confirm("Ouvrir toutes les sources ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()


def local_file_metadata():
    title("Local File Metadata", "Métadonnées de base d'un fichier local")
    raw = ask("Chemin complet du fichier")
    if not raw:
        wait()
        return
    file_path = Path(raw.strip('"')).expanduser()
    if not file_path.is_file():
        status("Fichier introuvable.", "error")
        wait()
        return
    stat = file_path.stat()
    data = {
        "file_name": file_path.name,
        "path": str(file_path.resolve()),
        "extension": file_path.suffix.lower(),
        "size_bytes": stat.st_size,
        "modified_local": datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(),
        "sha256": "",
        "image_exif": {},
    }
    digest = hashlib.sha256()
    with file_path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    data["sha256"] = digest.hexdigest()
    table = make_table("MÉTADONNÉES LOCALES", ["Champ", "Valeur"])
    table.add_row("Nom", data["file_name"])
    table.add_row("Extension", data["extension"] or "(aucune)")
    table.add_row("Taille", f"{stat.st_size:,} octets")
    table.add_row("Dernière modification", data["modified_local"])
    table.add_row("SHA-256", data["sha256"])
    try:
        from PIL import Image
        with Image.open(file_path) as image_obj:
            exif = image_obj.getexif()
            selected = {}
            for key, value in exif.items():
                selected[str(key)] = str(value)[:300]
            data["image_exif"] = selected
            if selected:
                table.add_row("EXIF image", json.dumps(selected, ensure_ascii=False)[:1500])
            else:
                table.add_row("EXIF image", "Aucune métadonnée EXIF lisible")
    except ImportError:
        table.add_row("EXIF image", "Pour lire l'EXIF : py -m pip install pillow")
    except Exception:
        table.add_row("EXIF image", "Non applicable ou illisible")
    console.print(table)
    console.print("[grey70]Les métadonnées peuvent contenir des informations personnelles : vérifie avant de partager un rapport.[/grey70]")
    maybe_save("local_file_metadata", data)
    wait()


# ---------------- RÉSEAU ----------------

def dns_lookup():
    title("DNS Intelligence", "Enregistrements DNS publics")
    domain = ask("Domaine")
    if not domain:
        wait()
        return
    records = {}
    table = make_table("DNS RECORDS", ["Type", "Valeurs"])
    if dns:
        for kind in ("A", "AAAA", "MX", "NS", "TXT"):
            try:
                values = [str(a) for a in dns.resolver.resolve(domain, kind)]
            except Exception:
                values = []
            records[kind] = values
            table.add_row(kind, "\n".join(values) if values else "Indisponible")
    else:
        try:
            values = sorted({x[4][0] for x in socket.getaddrinfo(domain, None)})
            records["IP"] = values
            table.add_row("IP", "\n".join(values))
        except Exception as error:
            records["error"] = str(error)
            table.add_row("Erreur", str(error))
        status("Installe dnspython pour MX/NS/TXT.", "warn")
    console.print(table)
    maybe_save("dns_lookup", {"domain": domain, "records": records})
    wait()

def ip_lookup():
    title("IP / Domain Intelligence", "Résolution et RDAP")
    host = ask("Adresse IP ou domaine")
    if not host:
        wait()
        return
    data = {"host": host}
    try:
        ip = socket.gethostbyname(host)
        data["ipv4"] = ip
        try:
            reverse = socket.gethostbyaddr(ip)[0]
        except Exception:
            reverse = "Non disponible"
        import ipaddress
        private = ipaddress.ip_address(ip).is_private
        data.update({"reverse_dns": reverse, "is_private": private})
        data["rdap_url"] = f"https://rdap.org/ip/{ip}"
        table = make_table("HOST INFORMATION", ["Champ", "Valeur"])
        table.add_row("IPv4", ip)
        table.add_row("DNS inverse", reverse)
        table.add_row("Type", "Privée" if private else "Publique")
        table.add_row("RDAP", data["rdap_url"])
        console.print(table)
        if confirm("Ouvrir RDAP ?"):
            webbrowser.open(data["rdap_url"])
    except Exception as error:
        status(str(error), "error")
    maybe_save("ip_lookup", data)
    wait()

def tcp_test():
    title("TCP Connection Test", "Test d'un hôte et d'un port")
    host = ask("Hôte")
    try:
        port = int(ask("Port", "443"))
        if not host or not 1 <= port <= 65535:
            raise ValueError("Hôte ou port invalide.")
        start = time.perf_counter()
        with socket.create_connection((host, port), timeout=4):
            elapsed = (time.perf_counter() - start) * 1000
        data = {"host": host, "port": port, "reachable": True, "latency_ms": round(elapsed, 2)}
        status(f"Port accessible — {elapsed:.1f} ms", "ok")
    except Exception as error:
        data = {"host": host, "reachable": False, "error": str(error)}
        status(str(error), "error")
    maybe_save("tcp_test", data)
    wait()

def discord_connection_test():
    title("Discord Connectivity", "Test de connexion au service")
    try:
        start = time.perf_counter()
        with socket.create_connection(("discord.com", 443), timeout=5):
            elapsed = (time.perf_counter() - start) * 1000
        data = {"host": "discord.com", "port": 443, "reachable": True, "latency_ms": round(elapsed, 2)}
        status(f"Connexion réussie — {elapsed:.1f} ms", "ok")
    except Exception as error:
        data = {"host": "discord.com", "port": 443, "reachable": False, "error": str(error)}
        status(str(error), "error")
    console.print("[grey62]Ce test ne révèle aucune donnée privée de compte.[/grey62]")
    maybe_save("discord_connectivity", data)
    wait()

def network_diagnostics():
    title("Network Diagnostics", "Contrôles réseau rapides")
    data = {}
    try:
        ip = socket.gethostbyname("discord.com")
        data["dns"] = ip
        status(f"DNS discord.com → {ip}", "ok")
    except Exception as error:
        data["dns_error"] = str(error)
        status(f"DNS : {error}", "error")
    try:
        from urllib.request import Request, urlopen
        req = Request("https://discord.com", headers={"User-Agent": "SYNERGIE-CLI"})
        with urlopen(req, timeout=5) as response:
            data["https_status"] = response.status
            status(f"HTTPS : statut {response.status}", "ok")
    except Exception as error:
        data["https_error"] = str(error)
        status(f"HTTPS : {error}", "error")
    maybe_save("network_diagnostics", data)
    wait()

# ---------------- SÉCURITÉ PC ----------------

SUSPICIOUS_EXTENSIONS = {".scr", ".vbs", ".vbe", ".js", ".jse", ".hta", ".bat", ".cmd", ".ps1", ".wsf", ".pif"}
SUSPICIOUS_PATTERNS = ("powershell -enc", "frombase64string", "invoke-expression", "downloadstring(", "createremotethread", "virtualalloc(", "keylogger")

def defender():
    title("Microsoft Defender", "État et analyse antivirus Windows")
    if os.name != "nt":
        status("Fonction disponible sous Windows uniquement.", "warn")
        wait()
        return
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled,AntivirusSignatureLastUpdated | Format-List"],
            capture_output=True, text=True, timeout=25
        )
        console.print(Panel(result.stdout or result.stderr or "Aucun résultat", title="DEFENDER STATUS", border_style="bright_cyan"))
    except Exception as error:
        status(str(error), "error")
    show_menu("DEFENDER ACTIONS", [("1", "Analyse rapide"), ("2", "Analyse complète"), ("3", "Ouvrir Sécurité Windows"), ("0", "Retour")])
    choice = ask("Action", "0")
    if choice in ("1", "2") and confirm("Lancer l'analyse ?", default=False):
        scan_type = "QuickScan" if choice == "1" else "FullScan"
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", f"Start-MpScan -ScanType {scan_type}"], check=False)
            status("Commande envoyée à Defender.", "ok")
        except Exception as error:
            status(str(error), "error")
    elif choice == "3":
        try:
            os.startfile("windowsdefender:")
        except Exception:
            webbrowser.open("windowsdefender:")
    wait()

def folder_scan():
    title("Folder Security Scan", "Analyse heuristique en lecture seule")
    folder = Path(ask("Chemin du dossier").strip('"'))
    if not folder.is_dir():
        status("Dossier introuvable.", "error")
        wait()
        return
    findings = []
    checked = 0
    try:
        with Progress(SpinnerColumn(), TextColumn("[bright_cyan]{task.description}"), console=console) as progress:
            task = progress.add_task("Analyse des fichiers...", total=None)
            for path in folder.rglob("*"):
                if checked >= 5000:
                    break
                if not path.is_file():
                    continue
                checked += 1
                reasons = []
                if path.suffix.lower() in SUSPICIOUS_EXTENSIONS:
                    reasons.append("extension à examiner")
                try:
                    if path.stat().st_size <= 2_000_000:
                        content = path.read_bytes().decode("utf-8", errors="ignore").lower()
                        reasons.extend(f"motif : {p}" for p in SUSPICIOUS_PATTERNS if p in content)
                except OSError:
                    pass
                if reasons:
                    findings.append({"file": str(path), "reasons": reasons})
            progress.update(task, completed=True)
    except OSError as error:
        status(str(error), "warn")
    table = make_table("SCAN RESULTS", ["Fichier", "Indicateurs"])
    for item in findings[:100]:
        table.add_row(item["file"], "\n".join(item["reasons"]))
    if not findings:
        table.add_row("Aucun signalement", "Aucun indicateur simple détecté")
    console.print(table)
    status(f"{checked} fichiers examinés ; {len(findings)} signalement(s).", "info")
    console.print("[grey62]Un signalement ne prouve pas qu'un fichier est malveillant. Aucun fichier n'est supprimé.[/grey62]")
    maybe_save("folder_scan", {"folder": str(folder), "checked": checked, "findings": findings})
    if os.name == "nt" and confirm("Lancer aussi une analyse rapide Defender ?", default=False):
        subprocess.run(["powershell", "-NoProfile", "-Command", "Start-MpScan -ScanType QuickScan"], check=False)
    wait()

def source_audit():
    title("Python Source Audit", "Analyse statique d'un script")
    path = Path(ask("Chemin du fichier .py").strip('"'))
    if not path.is_file() or path.suffix.lower() != ".py":
        status("Fichier Python introuvable.", "error")
        wait()
        return
    patterns = {
        "Exécution dynamique": r"\b(eval|exec)\s*\(",
        "Commande système": r"\bos\.system\s*\(",
        "Sous-processus": r"\bsubprocess\.(run|Popen|call)\s*\(",
        "Réseau": r"\b(requests\.|urllib\.request|socket\.)",
        "Base64": r"\bbase64\.",
    }
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        status(str(error), "error")
        wait()
        return
    findings = []
    table = make_table("SOURCE AUDIT", ["Indicateur", "Occurrences"])
    for label, pattern in patterns.items():
        count = len(re.findall(pattern, source))
        if count:
            findings.append({"category": label, "count": count})
            table.add_row(label, str(count))
    if not findings:
        table.add_row("Aucun indicateur simple", "0")
    console.print(table)
    console.print("[grey62]Cet audit ne prouve ni l'innocuité ni la dangerosité du script.[/grey62]")
    maybe_save("source_audit", {"file": str(path), "findings": findings})
    wait()

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def hash_file():
    title("SHA256 File Hash", "Calcul d'empreinte")
    path = Path(ask("Chemin du fichier").strip('"'))
    try:
        digest = sha256_file(path)
        table = make_table("FILE HASH", ["Champ", "Valeur"])
        table.add_row("Fichier", path.name)
        table.add_row("SHA256", digest)
        console.print(table)
        maybe_save("sha256", {"file": str(path), "sha256": digest})
    except Exception as error:
        status(str(error), "error")
    wait()

def analyze_file():
    title("File Inspector", "Métadonnées et signature simple")
    path = Path(ask("Chemin du fichier").strip('"'))
    if not path.is_file():
        status("Fichier introuvable.", "error")
        wait()
        return
    try:
        stat = path.stat()
        digest = sha256_file(path)
        with path.open("rb") as file:
            header = file.read(16)
        signatures = [
            (b"MZ", "Exécutable Windows potentiel"),
            (b"\x7fELF", "Exécutable ELF"),
            (b"PK\x03\x04", "Archive ZIP ou format dérivé"),
            (b"%PDF", "PDF"),
            (b"\x89PNG\r\n\x1a\n", "Image PNG"),
            (b"\xff\xd8\xff", "Image JPEG"),
        ]
        kind = next((label for sig, label in signatures if header.startswith(sig)), "Type inconnu")
        data = {
            "path": str(path),
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "sha256": digest,
            "type_guess": kind,
        }
        table = make_table("FILE DETAILS", ["Champ", "Valeur"])
        table.add_row("Nom", path.name)
        table.add_row("Taille", f"{stat.st_size:,} octets")
        table.add_row("Type estimé", kind)
        table.add_row("Modification", data["modified"])
        table.add_row("SHA256", digest)
        console.print(table)
        maybe_save("file_analysis", data)
    except Exception as error:
        status(str(error), "error")
    wait()

# ---------------- DISCORD OSINT ----------------

def discord_osint():
    title("Discord Account Intelligence", "Recherche d'informations publiques")
    show_menu("DISCORD MODULE", [
        ("1", "Analyser un ID Discord"),
        ("2", "Rechercher un pseudo publiquement"),
        ("3", "Ouvrir un profil par ID"),
        ("4", "Rechercher un identifiant sur le Web"),
        ("0", "Retour"),
    ])
    choice = ask("Sélection", "0")

    if choice == "0":
        return

    if choice == "1":
        user_id = ask("ID Discord")
        if not valid_discord_id(user_id):
            status("ID invalide.", "error")
            wait()
            return
        try:
            timestamp_ms = (int(user_id) >> 22) + 1420070400000
            created = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            age_days = (datetime.now(timezone.utc) - created).days
            profile = f"https://discord.com/users/{user_id}"
            data = {
                "discord_id": user_id,
                "estimated_creation_utc": created.isoformat(),
                "estimated_age_days": age_days,
                "profile_url": profile,
            }
            table = make_table("DISCORD ID REPORT", ["Champ", "Résultat"])
            table.add_row("ID", user_id)
            table.add_row("Création estimée", created.strftime("%d/%m/%Y %H:%M:%S UTC"))
            table.add_row("Âge estimé", f"{age_days} jours")
            table.add_row("Profil", profile)
            console.print(table)
            console.print(Panel(
                "[bright_yellow]L'ID seul ne révèle pas les e-mails, numéros, mots de passe, "
                "adresses IP, messages privés, amis ou serveurs privés.[/bright_yellow]",
                title="LIMITES DE L'ANALYSE",
                border_style="yellow",
            ))
            maybe_save("discord_id_analysis", data)
            if confirm("Ouvrir le profil Discord ?"):
                webbrowser.open(profile)
        except Exception as error:
            status(str(error), "error")

    elif choice == "2":
        username = ask("Pseudo Discord")
        if username:
            q = urllib.parse.quote_plus(f'"{username}" Discord')
            links = {
                "Google": f"https://www.google.com/search?q={q}",
                "Bing": f"https://www.bing.com/search?q={q}",
                "DuckDuckGo": f"https://duckduckgo.com/?q={q}",
                "Reddit": "https://www.reddit.com/search/?q=" + urllib.parse.quote_plus(username),
                "GitHub": "https://github.com/search?q=" + urllib.parse.quote_plus(username),
            }
            table = make_table("PUBLIC RESULTS", ["Source", "URL"])
            for site, url in links.items():
                table.add_row(site, url)
            console.print(table)
            maybe_save("discord_username_search", {"username": username, "links": links})
            if confirm("Ouvrir toutes les recherches ?"):
                for url in links.values():
                    webbrowser.open_new_tab(url)
            console.print("[grey62]Un pseudo identique ne prouve pas qu'il s'agit de la même personne.[/grey62]")

    elif choice == "3":
        user_id = ask("ID Discord")
        if valid_discord_id(user_id):
            open_link(f"https://discord.com/users/{user_id}")
        else:
            status("ID invalide.", "error")

    elif choice == "4":
        identifier = ask("Pseudo ou ID")
        if identifier:
            open_link("https://www.google.com/search?q=" + urllib.parse.quote_plus(f'"{identifier}" Discord'))
    else:
        status("Option inconnue.", "warn")

    wait()

# ---------------- OUTILS DISCORD SUPPLÉMENTAIRES ----------------

def discord_timestamp():
    title("Discord • Timestamp", "Créer un timestamp Discord depuis une date/heure")
    raw = ask("Date/heure ISO (ex. 2026-10-26 18:30)", datetime.now().strftime("%Y-%m-%d %H:%M"))
    try:
        dt = datetime.strptime(raw, "%Y-%m-%d %H:%M").astimezone()
        unix = int(dt.timestamp())
        table = make_table("TIMESTAMPS DISCORD", ["Style", "Code à copier", "Aperçu"])
        for code, label, preview in [
            ("t", "Heure courte", dt.strftime("%H:%M")),
            ("T", "Heure longue", dt.strftime("%H:%M:%S")),
            ("d", "Date courte", dt.strftime("%d/%m/%Y")),
            ("D", "Date longue", dt.strftime("%d %B %Y")),
            ("f", "Date + heure", dt.strftime("%d/%m/%Y %H:%M")),
            ("F", "Date complète", dt.strftime("%A %d %B %Y %H:%M")),
            ("R", "Relatif", "date relative"),
        ]:
            table.add_row(label, f"<t:{unix}:{code}>", preview)
        console.print(table)
        status("Copie un des codes dans Discord : il s'affichera selon le fuseau de chaque personne.", "ok")
        maybe_save("discord_timestamp", {"input": raw, "unix": unix})
    except ValueError:
        status("Format invalide. Utilise AAAA-MM-JJ HH:MM.", "error")
    wait()

def discord_message_link():
    title("Discord • Lien de message", "Construire un lien direct à partir des identifiants")
    guild = ask("ID du serveur (ou @me pour un message privé)")
    channel = ask("ID du salon")
    message = ask("ID du message")
    if not all(valid_discord_id(v) for v in (channel, message)) or (guild != "@me" and not valid_discord_id(guild)):
        status("Un ou plusieurs identifiants semblent invalides.", "error")
    else:
        url = f"https://discord.com/channels/{guild}/{channel}/{message}"
        console.print(Panel(url, title="LIEN DIRECT", border_style="bright_cyan"))
        if confirm("Ouvrir ce lien ?"):
            webbrowser.open(url)
    wait()

def discord_invite():
    title("Discord • Invitation", "Ouvrir ou préparer un lien d'invitation")
    invite = ask("Code ou URL d'invitation Discord")
    if invite:
        code = invite.strip().rstrip("/").split("/")[-1]
        if not re.fullmatch(r"[A-Za-z0-9-]{2,100}", code):
            status("Format de code d'invitation non reconnu.", "error")
        else:
            url = f"https://discord.gg/{code}"
            console.print(Panel(url, title="INVITATION", border_style="bright_blue"))
            status("La validité et les accès seront vérifiés par Discord dans le navigateur.", "info")
            if confirm("Ouvrir l'invitation ?"):
                webbrowser.open(url)
    wait()

def discord_profile_links():
    title("Discord • Liens de profil", "Préparer les liens publics d'un compte")
    user_id = ask("ID Discord (Snowflake)")
    if not valid_discord_id(user_id):
        status("ID invalide : un ID Discord contient généralement 17 à 20 chiffres.", "error")
        wait()
        return
    links = {
        "Profil Discord": f"https://discord.com/users/{user_id}",
        "Recherche Google de l'ID": "https://www.google.com/search?q=" + urllib.parse.quote_plus(f'"{user_id}" Discord'),
        "Recherche Reddit": "https://www.reddit.com/search/?q=" + urllib.parse.quote_plus(user_id),
    }
    table = make_table("LIENS PUBLICS", ["Type", "URL"])
    for label, url in links.items():
        table.add_row(label, url)
    console.print(table)
    if confirm("Ouvrir les liens dans le navigateur ?"):
        for url in links.values():
            webbrowser.open_new_tab(url)
    wait()

def discord_permissions():
    title("Discord • Permissions", "Lire une valeur de permissions (bitfield) publique")
    raw = ask("Valeur numérique des permissions")
    try:
        value = int(raw, 0)
        permissions = [
            ("Administrator", 8), ("Manage Guild", 32), ("Manage Roles", 268435456),
            ("Manage Channels", 16), ("Kick Members", 2), ("Ban Members", 4),
            ("Manage Messages", 8192), ("View Audit Log", 128),
            ("Manage Webhooks", 536870912), ("Mention Everyone", 131072),
            ("Connect", 1048576), ("Speak", 2097152), ("Manage Nicknames", 134217728),
            ("Moderate Members", 1099511627776),
        ]
        table = make_table("PERMISSIONS DÉTECTÉES", ["Permission", "Présente"])
        for label, bit in permissions:
            table.add_row(label, "[bright_green]OUI[/bright_green]" if value & bit else "[grey50]non[/grey50]")
        console.print(table)
        status("Lecture indicative d'un bitfield fourni par toi ; ce n'est pas une vérification d'accès en direct.", "info")
    except ValueError:
        status("Entre une valeur entière, décimale ou hexadécimale (ex. 0x8).", "error")
    wait()

def discord_resources():
    title("Discord • Ressources", "Raccourcis officiels et outils de développement")
    links = {
        "État des services Discord": "https://discordstatus.com/",
        "Centre d'aide Discord": "https://support.discord.com/hc/fr",
        "Portail développeur": "https://discord.com/developers/applications",
        "Documentation API": "https://discord.com/developers/docs/intro",
        "Guide communautaire": "https://discord.com/safety",
    }
    table = make_table("RESSOURCES OFFICIELLES", ["Ressource", "URL"])
    for label, url in links.items():
        table.add_row(label, url)
    console.print(table)
    choice = ask("Numéro à ouvrir (1-5, 0 pour rien)", "0")
    try:
        idx = int(choice)
        if 1 <= idx <= len(links):
            webbrowser.open(list(links.values())[idx - 1])
    except ValueError:
        status("Sélection invalide.", "warn")
    wait()

def discord_markdown():
    title("Discord • Markdown", "Prévisualiser les principaux formats de message")
    sample = Text()
    sample.append("**Texte en gras**\n", style="bold")
    sample.append("*Texte en italique*\n", style="italic")
    sample.append("__Texte souligné__\n", style="underline")
    sample.append("~~Texte barré~~\n", style="strike")
    sample.append("`code en ligne`\n", style="bright_cyan")
    sample.append("```\nbloc de code\n```\n", style="green")
    sample.append("||texte masqué||\n", style="grey70")
    sample.append("<t:1793030400:F>  (timestamp)", style="bright_magenta")
    console.print(Panel(sample, title="APERÇU DES SYNTAXES", border_style="bright_magenta"))
    status("Les styles exacts peuvent varier selon le contexte Discord.", "info")
    wait()


def discord_webhook_sender():
    """Envoie un message unique via un webhook Discord que l'utilisateur contrôle."""
    title("Discord • Webhook", "Envoyer un message via un webhook que tu es autorisé à utiliser")
    console.print(Panel(
        "[bold yellow]Important :[/bold yellow] un webhook n'est pas un bot Discord complet. "
        "Il permet de publier des messages dans le salon associé. Garde son URL secrète.",
        border_style="yellow"
    ))
    webhook_url = ask("URL du webhook Discord")
    if not webhook_url:
        status("Aucune URL fournie.", "warn")
        wait()
        return

    # Accepter uniquement les URL HTTPS des endpoints de webhook Discord.
    from urllib.parse import urlparse
    parsed = urlparse(webhook_url)
    allowed_hosts = {"discord.com", "discordapp.com"}
    if (parsed.scheme != "https" or parsed.hostname not in allowed_hosts or
            not re.fullmatch(r"/api/webhooks/\d+/[A-Za-z0-9._-]+/?", parsed.path)):
        status("URL refusée. Utilise l'URL HTTPS d'un webhook Discord officiel.", "error")
        wait()
        return

    message = ask("Message à envoyer (obligatoire)")
    if not message:
        status("Le message ne peut pas être vide.", "error")
        wait()
        return
    if len(message) > 2000:
        status("Le message dépasse la limite de 2000 caractères.", "error")
        wait()
        return

    username = ask("Nom affiché (facultatif, Entrée = nom du webhook)")
    payload = {"content": message, "allowed_mentions": {"parse": []}}
    if username:
        payload["username"] = username[:80]

    if not confirm("Envoyer ce message maintenant ?", default=False):
        status("Envoi annulé.", "info")
        wait()
        return

    try:
        from urllib.request import Request, urlopen
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = Request(
            webhook_url,
            data=body,
            headers={"Content-Type": "application/json", "User-Agent": "Synergie-Multitool/5.1"},
            method="POST",
        )
        with urlopen(request, timeout=15) as response:
            if response.status in (200, 204):
                status("Message envoyé sur Discord.", "ok")
            else:
                status(f"Réponse inattendue de Discord : HTTP {response.status}.", "warn")
    except Exception as error:
        # Ne jamais afficher ni enregistrer l'URL : elle contient le secret du webhook.
        status(f"Échec de l'envoi ({type(error).__name__}). Vérifie l'URL, la connexion et les droits du webhook.", "error")
    wait()


def discord_bot_builder():
    """Assistant guidé qui génère un véritable projet de bot Discord complet."""
    title("SYNERGIE • CRÉATEUR DE BOT DISCORD", "Assistant pas à pas — génération d'un projet prêt à configurer")
    console.print(Panel(
        "[bold bright_cyan]CE QUE TU VAS OBTENIR[/bold bright_cyan]\n"
        "• Un vrai bot Discord avec commandes slash (pas un webhook)\n"
        "• Annonces, sondages, salons, catégories et rôles\n"
        "• Modération : purge, verrouillage, slowmode, kick, ban et timeout\n"
        "• Infos serveur/membres, ping et message de bienvenue configurable\n"
        "• Un guide README, un modèle .env, les dépendances et un lanceur Windows\n\n"
        "[yellow]Le générateur ne demande jamais ton token. Tu le colleras toi-même dans le fichier .env du projet.[/yellow]",
        title="AVANT DE COMMENCER", border_style="bright_blue", box=box.ROUNDED, padding=(1, 2)
    ))
    console.print(Panel(
        "[bold]Étape 1/3 — Nom du projet[/bold]\nChoisis le nom du dossier qui contiendra tous les fichiers du bot.",
        border_style="bright_cyan", padding=(0, 2)
    ))
    project_name = ask("Nom du dossier", "synergie_discord_bot")
    project_name = re.sub(r"[^A-Za-z0-9_-]", "_", project_name).strip("_-") or "synergie_discord_bot"
    out_dir = ROOT / project_name
    if out_dir.exists() and any(out_dir.iterdir()):
        console.print(Panel(
            f"Le dossier [bold]{out_dir.name}[/bold] existe déjà.\nLes fichiers générés portant les mêmes noms seront remplacés si tu continues.",
            border_style="yellow"
        ))
        if not confirm("Continuer et remplacer les fichiers générés ?", default=False):
            status("Création annulée ; aucun fichier modifié.", "info")
            wait()
            return
    out_dir.mkdir(parents=True, exist_ok=True)

    console.print(Panel(
        "[bold]Étape 2/3 — Fonctionnalités incluses[/bold]\nTout est inclus ci-dessous ; les commandes sensibles vérifient les permissions Discord.",
        border_style="bright_magenta", padding=(0, 2)
    ))
    features = [
        ("Général", "/aide, /ping, /infoserveur, /infomembre"),
        ("Communauté", "/annonce, /sondage, /setbienvenue"),
        ("Organisation", "/creersalon, /creercategorie, /creerrole"),
        ("Modération", "/purge, /verrouiller, /deverrouiller, /slowmode, /kick, /ban, /timeout"),
    ]
    table = make_table("CONTENU DU BOT", ["Module", "Commandes"])
    for group_name, commands_text in features:
        table.add_row(group_name, commands_text)
    console.print(table)
    if not confirm("Générer le projet complet ?", default=True):
        status("Création annulée.", "info")
        wait()
        return

    bot_source = '# -*- coding: utf-8 -*-\n"""Bot Discord SYNERGIE — commandes slash avec contrôles de permissions."""\nimport json\nimport os\nfrom pathlib import Path\nfrom datetime import timedelta\n\nimport discord\nfrom discord import app_commands\nfrom discord.ext import commands\nfrom dotenv import load_dotenv\n\nBASE_DIR = Path(__file__).resolve().parent\nCONFIG_PATH = BASE_DIR / "config.json"\nload_dotenv(BASE_DIR / ".env")\nTOKEN = os.getenv("DISCORD_TOKEN", "").strip()\nGUILD_ID = os.getenv("DISCORD_GUILD_ID", "").strip()\n\nintents = discord.Intents.default()\nintents.members = True  # nécessaire pour les messages de bienvenue\nbot = commands.Bot(command_prefix="!", intents=intents)\nbot._synergie_commands_synced = False\n\n\ndef load_config():\n    try:\n        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))\n        return data if isinstance(data, dict) else {}\n    except (OSError, json.JSONDecodeError):\n        return {}\n\n\ndef save_config(data):\n    CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")\n\n\ndef member_can(interaction: discord.Interaction, permission: str) -> bool:\n    member = interaction.user\n    return isinstance(member, discord.Member) and bool(getattr(member.guild_permissions, permission, False))\n\n\n@bot.event\nasync def on_ready():\n    if not bot._synergie_commands_synced:\n        try:\n            if GUILD_ID.isdigit():\n                guild_object = discord.Object(id=int(GUILD_ID))\n                bot.tree.copy_global_to(guild=guild_object)\n                synced = await bot.tree.sync(guild=guild_object)\n                print(f"{len(synced)} commande(s) synchronisée(s) sur le serveur de test {GUILD_ID}.")\n            else:\n                synced = await bot.tree.sync()\n                print(f"{len(synced)} commande(s) globale(s) synchronisée(s). Leur apparition peut prendre un peu de temps.")\n            bot._synergie_commands_synced = True\n        except discord.HTTPException as exc:\n            print(f"Erreur de synchronisation des commandes : {exc}")\n    print(f"Connecté en tant que {bot.user} — SYNERGIE BOT actif.")\n\n\n@bot.event\nasync def on_member_join(member: discord.Member):\n    config = load_config()\n    channel_id = config.get(str(member.guild.id), {}).get("welcome_channel_id")\n    if not channel_id:\n        return\n    channel = member.guild.get_channel(int(channel_id))\n    if not isinstance(channel, discord.TextChannel):\n        return\n    embed = discord.Embed(\n        title="Bienvenue !",\n        description=f"Bienvenue {member.mention} sur **{member.guild.name}** !\\nNous sommes maintenant **{member.guild.member_count}** membres.",\n        color=discord.Color.blurple(),\n    )\n    embed.set_thumbnail(url=member.display_avatar.url)\n    try:\n        await channel.send(embed=embed, allowed_mentions=discord.AllowedMentions(users=True, roles=False, everyone=False))\n    except discord.HTTPException as exc:\n        print(f"Impossible d\'envoyer le message de bienvenue : {exc}")\n\n\n@bot.tree.command(name="aide", description="Afficher la liste des commandes SYNERGIE")\nasync def aide(interaction: discord.Interaction):\n    embed = discord.Embed(title="SYNERGIE BOT — Aide", color=discord.Color.blurple())\n    embed.description = (\n        "**Général**\\n`/aide` `/ping` `/infoserveur` `/infomembre`\\n\\n"\n        "**Communauté**\\n`/annonce` `/sondage` `/setbienvenue`\\n\\n"\n        "**Organisation**\\n`/creersalon` `/creercategorie` `/creerrole`\\n\\n"\n        "**Modération**\\n`/purge` `/verrouiller` `/deverrouiller` `/slowmode` `/kick` `/ban` `/timeout`"\n    )\n    embed.set_footer(text="Les commandes d\'administration nécessitent les permissions Discord adaptées.")\n    await interaction.response.send_message(embed=embed, ephemeral=True)\n\n\n@bot.tree.command(name="ping", description="Vérifier la latence du bot")\nasync def ping(interaction: discord.Interaction):\n    await interaction.response.send_message(f"Pong ! Latence : {round(bot.latency * 1000)} ms", ephemeral=True)\n\n\n@bot.tree.command(name="infoserveur", description="Afficher les informations du serveur")\nasync def infoserveur(interaction: discord.Interaction):\n    guild = interaction.guild\n    if guild is None:\n        return await interaction.response.send_message("Cette commande doit être utilisée dans un serveur.", ephemeral=True)\n    embed = discord.Embed(title=f"À propos de {guild.name}", color=discord.Color.blurple())\n    embed.add_field(name="Membres", value=str(guild.member_count or "Inconnu"))\n    embed.add_field(name="Salons", value=str(len(guild.channels)))\n    embed.add_field(name="Rôles", value=str(len(guild.roles)))\n    embed.add_field(name="Créé le", value=discord.utils.format_dt(guild.created_at, style="D"), inline=False)\n    if guild.icon:\n        embed.set_thumbnail(url=guild.icon.url)\n    await interaction.response.send_message(embed=embed, ephemeral=True)\n\n\n@bot.tree.command(name="infomembre", description="Afficher des informations publiques sur un membre")\n@app_commands.describe(membre="Membre à consulter (facultatif, par défaut toi-même)")\nasync def infomembre(interaction: discord.Interaction, membre: discord.Member | None = None):\n    if interaction.guild is None:\n        return await interaction.response.send_message("Cette commande doit être utilisée dans un serveur.", ephemeral=True)\n    target = membre or interaction.user\n    embed = discord.Embed(title=f"Membre : {target.display_name}", color=discord.Color.blurple())\n    embed.add_field(name="Nom", value=str(target), inline=True)\n    embed.add_field(name="ID", value=str(target.id), inline=True)\n    embed.add_field(name="Compte créé", value=discord.utils.format_dt(target.created_at, style="D"), inline=False)\n    if target.joined_at:\n        embed.add_field(name="A rejoint le serveur", value=discord.utils.format_dt(target.joined_at, style="D"), inline=False)\n    embed.set_thumbnail(url=target.display_avatar.url)\n    await interaction.response.send_message(embed=embed, ephemeral=True)\n\n\n@bot.tree.command(name="annonce", description="Publier une annonce mise en forme")\n@app_commands.describe(titre="Titre de l\'annonce", message="Texte de l\'annonce", salon="Salon cible (facultatif)")\n@app_commands.default_permissions(manage_guild=True)\nasync def annonce(interaction: discord.Interaction, titre: str, message: str, salon: discord.TextChannel | None = None):\n    if interaction.guild is None or not member_can(interaction, "manage_guild"):\n        return await interaction.response.send_message("Il faut la permission Gérer le serveur.", ephemeral=True)\n    destination = salon or interaction.channel\n    if not isinstance(destination, discord.TextChannel):\n        return await interaction.response.send_message("Choisis un salon textuel.", ephemeral=True)\n    embed = discord.Embed(title=titre[:256], description=message[:4000], color=discord.Color.blurple())\n    embed.set_footer(text=f"Annonce publiée par {interaction.user.display_name}")\n    try:\n        await destination.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())\n        await interaction.response.send_message(f"Annonce publiée dans {destination.mention}.", ephemeral=True)\n    except discord.Forbidden:\n        await interaction.response.send_message("Je n\'ai pas la permission d\'écrire dans ce salon.", ephemeral=True)\n    except discord.HTTPException:\n        await interaction.response.send_message("Discord n\'a pas accepté l\'annonce. Vérifie le texte et réessaie.", ephemeral=True)\n\n\n@bot.tree.command(name="sondage", description="Créer un sondage Oui/Non")\n@app_commands.describe(question="Question du sondage")\n@app_commands.default_permissions(manage_messages=True)\nasync def sondage(interaction: discord.Interaction, question: str):\n    if interaction.guild is None or not member_can(interaction, "manage_messages"):\n        return await interaction.response.send_message("Il faut la permission Gérer les messages.", ephemeral=True)\n    if not isinstance(interaction.channel, (discord.TextChannel, discord.Thread)):\n        return await interaction.response.send_message("Cette commande doit être utilisée dans un salon textuel.", ephemeral=True)\n    embed = discord.Embed(title="📊 Sondage", description=question[:4000], color=discord.Color.green())\n    embed.set_footer(text=f"Lancé par {interaction.user.display_name}")\n    try:\n        message = await interaction.channel.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())\n        await message.add_reaction("👍")\n        await message.add_reaction("👎")\n        await interaction.response.send_message("Sondage créé.", ephemeral=True)\n    except discord.Forbidden:\n        await interaction.response.send_message("Je n\'ai pas la permission d\'envoyer le sondage ou d\'ajouter les réactions.", ephemeral=True)\n\n\n@bot.tree.command(name="creersalon", description="Créer un salon textuel ou vocal")\n@app_commands.describe(nom="Nom du salon", type_salon="Type de salon", categorie="Catégorie de destination (facultatif)")\n@app_commands.choices(type_salon=[app_commands.Choice(name="Textuel", value="texte"), app_commands.Choice(name="Vocal", value="vocal")])\n@app_commands.default_permissions(manage_channels=True)\nasync def creersalon(interaction: discord.Interaction, nom: str, type_salon: app_commands.Choice[str], categorie: discord.CategoryChannel | None = None):\n    if interaction.guild is None or not member_can(interaction, "manage_channels"):\n        return await interaction.response.send_message("Il faut la permission Gérer les salons.", ephemeral=True)\n    safe_name = "-".join(nom.lower().split())[:90]\n    if not safe_name:\n        return await interaction.response.send_message("Le nom du salon ne peut pas être vide.", ephemeral=True)\n    try:\n        if type_salon.value == "vocal":\n            channel = await interaction.guild.create_voice_channel(safe_name, category=categorie, reason=f"Demandé par {interaction.user}")\n        else:\n            channel = await interaction.guild.create_text_channel(safe_name, category=categorie, reason=f"Demandé par {interaction.user}")\n        await interaction.response.send_message(f"Salon créé : {channel.mention}", ephemeral=True)\n    except discord.Forbidden:\n        await interaction.response.send_message("Je ne peux pas créer ce salon. Vérifie la permission Gérer les salons et la hiérarchie.", ephemeral=True)\n    except discord.HTTPException:\n        await interaction.response.send_message("Discord n\'a pas pu créer ce salon. Réessaie avec un nom plus simple.", ephemeral=True)\n\n\n@bot.tree.command(name="creercategorie", description="Créer une catégorie de salons")\n@app_commands.describe(nom="Nom de la catégorie")\n@app_commands.default_permissions(manage_channels=True)\nasync def creercategorie(interaction: discord.Interaction, nom: str):\n    if interaction.guild is None or not member_can(interaction, "manage_channels"):\n        return await interaction.response.send_message("Il faut la permission Gérer les salons.", ephemeral=True)\n    try:\n        category = await interaction.guild.create_category(name=nom[:100], reason=f"Demandé par {interaction.user}")\n        await interaction.response.send_message(f"Catégorie créée : **{category.name}**", ephemeral=True)\n    except discord.Forbidden:\n        await interaction.response.send_message("Je n\'ai pas la permission de créer une catégorie.", ephemeral=True)\n\n\n@bot.tree.command(name="creerrole", description="Créer un rôle sans permission sensible")\n@app_commands.describe(nom="Nom du rôle", couleur="Couleur hexadécimale, ex. #5865F2")\n@app_commands.default_permissions(manage_roles=True)\nasync def creerrole(interaction: discord.Interaction, nom: str, couleur: str = "#5865F2"):\n    if interaction.guild is None or not member_can(interaction, "manage_roles"):\n        return await interaction.response.send_message("Il faut la permission Gérer les rôles.", ephemeral=True)\n    raw = couleur.lstrip("#")\n    if len(raw) != 6 or any(char not in "0123456789abcdefABCDEF" for char in raw):\n        return await interaction.response.send_message("Couleur invalide. Exemple : #5865F2.", ephemeral=True)\n    try:\n        role = await interaction.guild.create_role(name=nom[:100], colour=discord.Colour(int(raw, 16)), reason=f"Demandé par {interaction.user}")\n        await interaction.response.send_message(f"Rôle créé : {role.mention}. Aucune permission administrative n\'a été accordée.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())\n    except discord.Forbidden:\n        await interaction.response.send_message("Je ne peux pas créer ce rôle. Vérifie mes permissions et la hiérarchie des rôles.", ephemeral=True)\n\n\n@bot.tree.command(name="purge", description="Supprimer de 1 à 100 messages récents")\n@app_commands.describe(nombre="Nombre de messages à supprimer (1 à 100)")\n@app_commands.default_permissions(manage_messages=True)\nasync def purge(interaction: discord.Interaction, nombre: app_commands.Range[int, 1, 100]):\n    if interaction.guild is None or not member_can(interaction, "manage_messages"):\n        return await interaction.response.send_message("Il faut la permission Gérer les messages.", ephemeral=True)\n    if not isinstance(interaction.channel, discord.TextChannel):\n        return await interaction.response.send_message("Utilise cette commande dans un salon textuel classique.", ephemeral=True)\n    await interaction.response.defer(ephemeral=True)\n    try:\n        deleted = await interaction.channel.purge(limit=nombre)\n        await interaction.followup.send(f"{len(deleted)} message(s) supprimé(s).", ephemeral=True)\n    except discord.Forbidden:\n        await interaction.followup.send("Je n\'ai pas la permission de gérer les messages.", ephemeral=True)\n    except discord.HTTPException:\n        await interaction.followup.send("Discord n\'a pas pu supprimer les messages.", ephemeral=True)\n\n\nasync def set_lock(interaction: discord.Interaction, locked: bool):\n    if interaction.guild is None or not member_can(interaction, "manage_channels"):\n        return await interaction.response.send_message("Il faut la permission Gérer les salons.", ephemeral=True)\n    channel = interaction.channel\n    if not isinstance(channel, discord.TextChannel):\n        return await interaction.response.send_message("Utilise cette commande dans un salon textuel.", ephemeral=True)\n    overwrite = channel.overwrites_for(interaction.guild.default_role)\n    overwrite.send_messages = False if locked else None\n    try:\n        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason=f"{\'Verrouillage\' if locked else \'Déverrouillage\'} par {interaction.user}")\n        await interaction.response.send_message("🔒 Salon verrouillé." if locked else "🔓 Salon déverrouillé.", allowed_mentions=discord.AllowedMentions.none())\n    except discord.Forbidden:\n        await interaction.response.send_message("Je n\'ai pas la permission de modifier ce salon.", ephemeral=True)\n\n\n@bot.tree.command(name="verrouiller", description="Empêcher @everyone d\'écrire dans le salon")\n@app_commands.default_permissions(manage_channels=True)\nasync def verrouiller(interaction: discord.Interaction):\n    await set_lock(interaction, True)\n\n\n@bot.tree.command(name="deverrouiller", description="Autoriser de nouveau @everyone à écrire")\n@app_commands.default_permissions(manage_channels=True)\nasync def deverrouiller(interaction: discord.Interaction):\n    await set_lock(interaction, False)\n\n\n@bot.tree.command(name="slowmode", description="Régler le délai entre les messages du salon")\n@app_commands.describe(secondes="Délai en secondes (0 à 21600)")\n@app_commands.default_permissions(manage_channels=True)\nasync def slowmode(interaction: discord.Interaction, secondes: app_commands.Range[int, 0, 21600]):\n    if interaction.guild is None or not member_can(interaction, "manage_channels"):\n        return await interaction.response.send_message("Il faut la permission Gérer les salons.", ephemeral=True)\n    if not isinstance(interaction.channel, discord.TextChannel):\n        return await interaction.response.send_message("Utilise cette commande dans un salon textuel.", ephemeral=True)\n    try:\n        await interaction.channel.edit(slowmode_delay=secondes, reason=f"Slowmode réglé par {interaction.user}")\n        await interaction.response.send_message(f"Slowmode réglé sur {secondes} seconde(s).", ephemeral=True)\n    except discord.Forbidden:\n        await interaction.response.send_message("Je n\'ai pas la permission de modifier ce salon.", ephemeral=True)\n\n\n@bot.tree.command(name="kick", description="Exclure un membre du serveur")\n@app_commands.describe(membre="Membre à exclure", raison="Raison de l\'exclusion")\n@app_commands.default_permissions(kick_members=True)\nasync def kick(interaction: discord.Interaction, membre: discord.Member, raison: str = "Aucune raison précisée"):\n    if interaction.guild is None or not member_can(interaction, "kick_members"):\n        return await interaction.response.send_message("Il faut la permission Expulser des membres.", ephemeral=True)\n    if membre == interaction.user or membre == interaction.guild.owner:\n        return await interaction.response.send_message("Tu ne peux pas expulser cette personne.", ephemeral=True)\n    try:\n        await membre.kick(reason=f"{raison[:400]} — demandé par {interaction.user}")\n        await interaction.response.send_message(f"{membre} a été expulsé. Raison : {raison[:300]}", ephemeral=True)\n    except discord.Forbidden:\n        await interaction.response.send_message("Action refusée : vérifie la hiérarchie des rôles et la permission Expulser.", ephemeral=True)\n\n\n@bot.tree.command(name="ban", description="Bannir un membre du serveur")\n@app_commands.describe(membre="Membre à bannir", raison="Raison du bannissement")\n@app_commands.default_permissions(ban_members=True)\nasync def ban(interaction: discord.Interaction, membre: discord.Member, raison: str = "Aucune raison précisée"):\n    if interaction.guild is None or not member_can(interaction, "ban_members"):\n        return await interaction.response.send_message("Il faut la permission Bannir des membres.", ephemeral=True)\n    if membre == interaction.user or membre == interaction.guild.owner:\n        return await interaction.response.send_message("Tu ne peux pas bannir cette personne.", ephemeral=True)\n    try:\n        await interaction.guild.ban(membre, reason=f"{raison[:400]} — demandé par {interaction.user}")\n        await interaction.response.send_message(f"{membre} a été banni. Raison : {raison[:300]}", ephemeral=True)\n    except discord.Forbidden:\n        await interaction.response.send_message("Action refusée : vérifie la hiérarchie des rôles et la permission Bannir.", ephemeral=True)\n\n\n@bot.tree.command(name="timeout", description="Mettre un membre en timeout jusqu\'à 28 jours")\n@app_commands.describe(membre="Membre à mettre en timeout", minutes="Durée en minutes (1 à 40320)", raison="Raison")\n@app_commands.default_permissions(moderate_members=True)\nasync def timeout(interaction: discord.Interaction, membre: discord.Member, minutes: app_commands.Range[int, 1, 40320], raison: str = "Aucune raison précisée"):\n    if interaction.guild is None or not member_can(interaction, "moderate_members"):\n        return await interaction.response.send_message("Il faut la permission Modérer les membres.", ephemeral=True)\n    if membre == interaction.user or membre == interaction.guild.owner:\n        return await interaction.response.send_message("Tu ne peux pas mettre cette personne en timeout.", ephemeral=True)\n    try:\n        await membre.timeout(timedelta(minutes=minutes), reason=f"{raison[:400]} — demandé par {interaction.user}")\n        await interaction.response.send_message(f"{membre.mention} est en timeout pour {minutes} minute(s).", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())\n    except discord.Forbidden:\n        await interaction.response.send_message("Action refusée : vérifie la hiérarchie des rôles et la permission Modérer les membres.", ephemeral=True)\n\n\n@bot.tree.command(name="setbienvenue", description="Choisir le salon des messages de bienvenue")\n@app_commands.describe(salon="Salon où les nouveaux membres seront accueillis")\n@app_commands.default_permissions(manage_guild=True)\nasync def setbienvenue(interaction: discord.Interaction, salon: discord.TextChannel):\n    if interaction.guild is None or not member_can(interaction, "manage_guild"):\n        return await interaction.response.send_message("Il faut la permission Gérer le serveur.", ephemeral=True)\n    config = load_config()\n    guild_config = config.setdefault(str(interaction.guild.id), {})\n    guild_config["welcome_channel_id"] = salon.id\n    try:\n        save_config(config)\n        await interaction.response.send_message(f"Les messages de bienvenue seront publiés dans {salon.mention}.", ephemeral=True)\n    except OSError:\n        await interaction.response.send_message("Impossible d\'enregistrer la configuration. Vérifie les droits d\'écriture du dossier du bot.", ephemeral=True)\n\n\n@bot.tree.error\nasync def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):\n    message = "Une erreur est survenue. Vérifie les permissions du bot et réessaie."\n    print(f"Erreur de commande : {type(error).__name__}: {error}")\n    try:\n        if interaction.response.is_done():\n            await interaction.followup.send(message, ephemeral=True)\n        else:\n            await interaction.response.send_message(message, ephemeral=True)\n    except discord.HTTPException:\n        pass\n\n\nif __name__ == "__main__":\n    if not TOKEN or TOKEN == "COLLE_ICI_LE_TOKEN":\n        raise SystemExit("Token manquant : ouvre le fichier .env et renseigne DISCORD_TOKEN. Ne partage jamais ce token.")\n    try:\n        bot.run(TOKEN)\n    except discord.LoginFailure:\n        raise SystemExit("Connexion refusée : token invalide. Génère un nouveau token dans le Portail développeur Discord.")\n'
    readme = "# __PROJECT__ — Bot Discord SYNERGIE\n\nBienvenue ! Ce dossier contient un vrai bot Discord basé sur `discord.py`, avec des commandes slash. Ce n'est pas un webhook.\n\n## 1. Ce qu'il sait faire\n\n### Général\n- `/aide` : liste des commandes\n- `/ping` : latence du bot\n- `/infoserveur` : nombre de membres, salons, rôles et date de création\n- `/infomembre` : informations publiques d'un membre\n\n### Communauté\n- `/annonce` : publie une annonce mise en forme, avec choix du salon\n- `/sondage` : crée un sondage Oui/Non avec réactions\n- `/setbienvenue` : configure le salon où les nouveaux membres sont accueillis\n\n### Organisation\n- `/creersalon` : crée un salon textuel ou vocal, avec catégorie facultative\n- `/creercategorie` : crée une catégorie\n- `/creerrole` : crée un rôle coloré sans permissions administratives\n\n### Modération\n- `/purge` : supprime de 1 à 100 messages récents\n- `/verrouiller` et `/deverrouiller` : bloque/rétablit l'écriture de @everyone dans le salon\n- `/slowmode` : règle le délai entre les messages\n- `/kick` : expulse un membre\n- `/ban` : bannit un membre\n- `/timeout` : limite temporairement un membre (jusqu'à 28 jours)\n\nLes commandes sensibles vérifient les permissions du membre et nécessitent également les permissions correspondantes pour le bot. La hiérarchie des rôles Discord s'applique.\n\n## 2. Installer Python\n\nInstalle Python 3.10 ou plus récent depuis https://www.python.org/downloads/. Sur Windows, coche **Add Python to PATH** pendant l'installation si cette option est proposée.\n\n## 3. Créer l'application Discord\n\n1. Ouvre https://discord.com/developers/applications et connecte-toi.\n2. Clique sur **New Application**, donne-lui un nom et valide.\n3. Ouvre l'onglet **Bot** puis crée le bot si nécessaire.\n4. Dans la section du bot, utilise **Reset Token** / **View Token** pour obtenir le token. Copie-le dans ton fichier `.env` local. **Ne l'envoie à personne et ne le publie jamais.**\n5. Toujours dans **Bot**, active **Server Members Intent** dans les intents privilégiés : il est nécessaire pour les messages de bienvenue.\n6. Dans **OAuth2 → URL Generator**, coche les scopes `bot` et `applications.commands`.\n7. Sélectionne uniquement les permissions nécessaires : View Channels, Send Messages, Embed Links, Read Message History, Add Reactions, Manage Channels, Manage Roles, Manage Messages, Kick Members, Ban Members et Moderate Members.\n8. Copie l'URL générée, ouvre-la et ajoute le bot à ton serveur. Ne lui donne pas Administrator si ce n'est pas nécessaire.\n\n## 4. Configurer le token\n\n1. Dans ce dossier, copie `.env.example` et nomme la copie `.env`.\n2. Ouvre `.env` avec le Bloc-notes.\n3. Remplace `COLLE_ICI_LE_TOKEN` par le token du bot, sans ajouter de guillemets.\n4. Pour tester les commandes rapidement, ajoute l'ID de ton serveur dans `DISCORD_GUILD_ID`. Laisse cette valeur vide pour synchroniser les commandes globalement (elles peuvent mettre du temps à apparaître).\n\nPour récupérer l'ID d'un serveur : dans Discord, active **Paramètres → Avancés → Mode développeur**, puis clic droit sur le serveur → **Copier l'identifiant du serveur**.\n\n## 5. Démarrer le bot sur Windows\n\nDouble-clique sur `start.bat`, ou ouvre un terminal dans ce dossier et exécute :\n\n```bat\npy -m pip install -r requirements.txt\npy bot.py\n```\n\nGarde la fenêtre ouverte tant que tu veux que le bot reste connecté. Pour l'arrêter, utilise `Ctrl+C`.\n\n## 6. Configurer le message de bienvenue\n\nUne fois le bot en ligne, utilise `/setbienvenue` dans ton serveur et choisis un salon. Le réglage est enregistré dans `config.json`.\n\n## Dépannage\n\n- **Token invalide** : génère un nouveau token dans le Portail développeur, puis mets-le dans `.env`.\n- **Commandes invisibles** : vérifie que tu as invité le bot avec `applications.commands`. Un ID de serveur dans `.env` permet une synchronisation de test plus rapide.\n- **Action refusée** : vérifie les permissions du bot et place son rôle au-dessus des rôles qu'il doit gérer/modérer.\n- **Bienvenue non envoyé** : vérifie que Server Members Intent est activé dans le Portail développeur et que le bot peut écrire dans le salon choisi.\n\nNe partage jamais `.env`. Le fichier est exclu du contrôle de version par `.gitignore`.\n".replace("__PROJECT__", project_name)
    env_example = "# Token du bot (secret) — ne publie jamais ce fichier après y avoir mis le token\nDISCORD_TOKEN=COLLE_ICI_LE_TOKEN\n\n# Facultatif : ID du serveur de test pour synchroniser les commandes plus vite\nDISCORD_GUILD_ID=\n"
    requirements = "discord.py>=2.4,<3.0\npython-dotenv>=1.0,<2.0\n"
    gitignore = ".env\n.venv/\n__pycache__/\n*.pyc\nconfig.json\n"
    start_bat = "@echo off\nchcp 65001 >nul\ncd /d \"%~dp0\"\necho ========================================\necho      SYNERGIE - LANCEMENT DU BOT\necho ========================================\npy -m pip install -r requirements.txt\nif errorlevel 1 (\n  echo Erreur pendant l'installation des dependances.\n  pause\n  exit /b 1\n)\necho.\npy bot.py\necho.\necho Le bot s'est arrete. Lis le message ci-dessus pour comprendre pourquoi.\npause\n"
    config_json = "{\n}\n"
    files_to_write = {
        "bot.py": bot_source,
        "README.md": readme,
        ".env.example": env_example,
        "requirements.txt": requirements,
        ".gitignore": gitignore,
        "start.bat": start_bat,
        "config.json": config_json,
    }
    try:
        for filename, content in files_to_write.items():
            (out_dir / filename).write_text(content, encoding="utf-8")
    except OSError as error:
        status(f"Impossible d'écrire le projet : {error}", "error")
        wait()
        return

    console.print(Panel(
        f"[bold bright_green]Projet créé : {out_dir}[/bold bright_green]\n\n"
        "[bold]Fichiers générés[/bold]\n"
        "• bot.py — code complet du bot\n"
        "• README.md — guide détaillé étape par étape\n"
        "• .env.example — modèle pour le token et l'ID de test\n"
        "• requirements.txt — dépendances nécessaires\n"
        "• start.bat — installation et lancement sous Windows\n"
        "• config.json — configuration des messages de bienvenue\n"
        "• .gitignore — exclut les secrets et fichiers temporaires\n\n"
        "[bold bright_yellow]ÉTAPE SUIVANTE[/bold bright_yellow]\n"
        "1. Ouvre le dossier généré.\n"
        "2. Copie .env.example en .env et ajoute ton token.\n"
        "3. Lis README.md pour créer/inviter l'application Discord.\n"
        "4. Double-clique sur start.bat.",
        title="BOT DISCORD GÉNÉRÉ", border_style="bright_green", box=box.DOUBLE, padding=(1, 2)
    ))
    if confirm("Ouvrir le dossier du projet maintenant ?", default=True):
        try:
            if os.name == "nt":
                os.startfile(str(out_dir))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(out_dir)])
            else:
                subprocess.Popen(["xdg-open", str(out_dir)])
        except Exception as error:
            status(f"Dossier créé, mais impossible de l'ouvrir automatiquement : {error}", "warn")
    wait()



# ---------------- RECHERCHE TÉLÉPHONIQUE ----------------

def phone_lookup():
    title("Phone Number Intelligence", "Analyse de format et métadonnées publiques")
    try:
        import phonenumbers
        from phonenumbers import carrier, geocoder, timezone as phone_timezone
        from phonenumbers import PhoneNumberType
    except ImportError:
        status("Module manquant. Installe-le avec : py -m pip install phonenumbers", "error")
        wait()
        return

    raw_number = ask("Numéro de téléphone (ex. +33612345678)")
    if not raw_number:
        wait()
        return

    default_region = ask("Pays si le numéro n'a pas d'indicatif (ex. FR)", "FR").upper()
    try:
        parsed = phonenumbers.parse(raw_number, default_region or "FR")
    except phonenumbers.NumberParseException as error:
        status(f"Impossible d'analyser ce numéro : {error}", "error")
        wait()
        return

    possible = phonenumbers.is_possible_number(parsed)
    valid = phonenumbers.is_valid_number(parsed)
    type_names = {
        PhoneNumberType.FIXED_LINE: "Fixe",
        PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou mobile",
        PhoneNumberType.TOLL_FREE: "Numéro gratuit",
        PhoneNumberType.PREMIUM_RATE: "Numéro surtaxé",
        PhoneNumberType.SHARED_COST: "Coût partagé",
        PhoneNumberType.VOIP: "VoIP",
        PhoneNumberType.PERSONAL_NUMBER: "Numéro personnel",
        PhoneNumberType.PAGER: "Pager",
        PhoneNumberType.UAN: "Numéro d'accès universel",
        PhoneNumberType.VOICEMAIL: "Messagerie vocale",
        PhoneNumberType.UNKNOWN: "Inconnu",
    }
    number_type = type_names.get(phonenumbers.number_type(parsed), "Inconnu")
    country = geocoder.description_for_number(parsed, "fr") or "Non déterminé"
    # Cette donnée décrit généralement l'opérateur d'origine ou l'allocation du numéro,
    # et non nécessairement l'opérateur actuel après portabilité.
    original_carrier = carrier.name_for_number(parsed, "fr") or "Non disponible dans les métadonnées"
    zones = list(phone_timezone.time_zones_for_number(parsed))
    international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    data = {
        "input": raw_number,
        "international_format": international,
        "national_format": national,
        "e164": e164,
        "country_or_region": country,
        "country_calling_code": f"+{parsed.country_code}",
        "possible_number": possible,
        "valid_number_according_to_metadata": valid,
        "line_type": number_type,
        "carrier_metadata": original_carrier,
        "time_zones": zones,
        "limitations": (
            "L'opérateur affiché peut être celui d'origine/de l'allocation. "
            "La portabilité peut rendre l'opérateur actuel impossible à déterminer "
            "avec les seules métadonnées locales."
        ),
    }

    table = make_table("PHONE NUMBER REPORT", ["Champ", "Résultat"])
    table.add_row("Numéro international", international)
    table.add_row("Format national", national)
    table.add_row("Format E.164", e164)
    table.add_row("Indicatif", f"+{parsed.country_code}")
    table.add_row("Pays / région", country)
    table.add_row("Numéro possible", "Oui" if possible else "Non")
    table.add_row("Numéro valide selon les métadonnées", "Oui" if valid else "Non")
    table.add_row("Type de ligne", number_type)
    table.add_row("Opérateur (métadonnées)", original_carrier)
    table.add_row("Fuseaux horaires", ", ".join(zones) if zones else "Non disponible")
    console.print(table)
    console.print(Panel(
        "[yellow]Limites : l'analyse ne permet pas d'identifier le titulaire, "
        "son adresse ou sa localisation en temps réel. L'opérateur indiqué peut être "
        "inexact après portabilité. Pour l'opérateur actuel, il faut une source autorisée "
        "et à jour prenant en charge la portabilité.[/yellow]",
        title="INFORMATIONS IMPORTANTES",
        border_style="yellow",
    ))

    search_url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(f'"{international}" opérateur')
    data["public_search_url"] = search_url
    maybe_save("phone_number_analysis", data)
    if confirm("Ouvrir une recherche Web publique sur ce numéro ?", default=False):
        webbrowser.open(search_url)
    wait()



def _phone_lib():
    try:
        import phonenumbers
        from phonenumbers import carrier, geocoder, timezone as phone_timezone
        return phonenumbers, carrier, geocoder, phone_timezone
    except ImportError:
        status("Module manquant. Installe-le avec : py -m pip install phonenumbers", "error")
        return None


def _parse_phone(raw, region="FR"):
    lib = _phone_lib()
    if not lib:
        return None, None
    phonenumbers = lib[0]
    try:
        parsed = phonenumbers.parse(raw, (region or "FR").upper())
        return phonenumbers, parsed
    except phonenumbers.NumberParseException as exc:
        status(f"Numéro impossible à analyser : {exc}", "error")
        return phonenumbers, None


def phone_format_converter():
    title("PHONE • FORMAT CONVERTER", "Convertir un numéro entre formats internationaux")
    raw = ask("Numéro de téléphone")
    if not raw:
        wait(); return
    region = ask("Pays par défaut si pas d'indicatif (ex. FR)", "FR")
    lib, parsed = _parse_phone(raw, region)
    if not lib or not parsed:
        wait(); return
    table = make_table("FORMATS", ["Format", "Valeur"])
    for label, fmt in [("International", lib.PhoneNumberFormat.INTERNATIONAL), ("National", lib.PhoneNumberFormat.NATIONAL), ("E.164", lib.PhoneNumberFormat.E164), ("RFC3966 / tel:", lib.PhoneNumberFormat.RFC3966)]:
        table.add_row(label, lib.format_number(parsed, fmt))
    console.print(table)
    maybe_save("phone_formats", {"input": raw, "region": region, "formats": {"international": lib.format_number(parsed, lib.PhoneNumberFormat.INTERNATIONAL), "national": lib.format_number(parsed, lib.PhoneNumberFormat.NATIONAL), "e164": lib.format_number(parsed, lib.PhoneNumberFormat.E164), "rfc3966": lib.format_number(parsed, lib.PhoneNumberFormat.RFC3966)}})
    wait()


def phone_batch_validate():
    title("PHONE • BATCH CHECK", "Vérifier plusieurs numéros saisis localement")
    console.print("[grey62]Entre un numéro par ligne. Les données restent sur cette machine, sauf si tu choisis de sauvegarder le rapport.[/grey62]")
    region = ask("Pays par défaut", "FR").upper()
    raw = ask("Numéros séparés par des virgules")
    if not raw:
        wait(); return
    lib = _phone_lib()
    if not lib:
        wait(); return
    phonenumbers = lib[0]
    table = make_table("RÉSULTATS", ["Entrée", "Possible", "Valide*", "Format international"])
    results=[]
    for item in [x.strip() for x in raw.split(",") if x.strip()]:
        try:
            parsed = phonenumbers.parse(item, region or "FR")
            possible = phonenumbers.is_possible_number(parsed)
            valid = phonenumbers.is_valid_number(parsed)
            intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            table.add_row(item, "Oui" if possible else "Non", "Oui" if valid else "Non", intl)
            results.append({"input":item,"possible":possible,"valid_by_metadata":valid,"international":intl})
        except phonenumbers.NumberParseException as exc:
            table.add_row(item, "—", "Non", f"Erreur : {exc}")
            results.append({"input":item,"possible":False,"valid_by_metadata":False,"error":str(exc)})
    console.print(table)
    console.print("[grey62]*La validité est évaluée selon les métadonnées téléphoniques, pas par un appel ou un SMS.[/grey62]")
    maybe_save("phone_batch_check", {"default_region":region,"results":results})
    wait()


def phone_country_reference():
    title("PHONE • INDICATIFS PAYS", "Référence locale des indicatifs téléphoniques")
    lib = _phone_lib()
    if not lib:
        wait(); return
    phonenumbers=lib[0]
    query=ask("Code pays ISO (ex. FR) ou indicatif (ex. +33)", "FR").upper().strip()
    table=make_table("RÉFÉRENCE", ["Code pays", "Indicatif", "Région(s)"])
    matches=[]
    if query.startswith("+") or query.isdigit():
        code=query.lstrip("+")
        if code.isdigit() and int(code) in phonenumbers.COUNTRY_CODE_TO_REGION_CODE:
            regions=phonenumbers.COUNTRY_CODE_TO_REGION_CODE[int(code)]
            table.add_row(", ".join(regions), f"+{code}", ", ".join(regions)); matches.append({"regions":list(regions),"calling_code":"+"+code})
    else:
        code=phonenumbers.country_code_for_region(query)
        if code:
            table.add_row(query, f"+{code}", query); matches.append({"region":query,"calling_code":f"+{code}"})
    if not matches:
        table.add_row("Aucun résultat", "—", "Vérifie le code ISO ou l'indicatif.")
    console.print(table)
    wait()


def phone_example_generator():
    title("PHONE • EXEMPLES", "Générer un numéro d'exemple issu des métadonnées")
    lib = _phone_lib()
    if not lib:
        wait(); return
    phonenumbers=lib[0]
    from phonenumbers import PhoneNumberType
    region=ask("Code pays ISO (ex. FR)", "FR").upper()
    kind=ask("Type (mobile / fixe)", "mobile").lower()
    phone_type=PhoneNumberType.FIXED_LINE if kind in ("fixe","fixed","landline") else PhoneNumberType.MOBILE
    example=phonenumbers.example_number_for_type(region, phone_type)
    if not example:
        example=phonenumbers.example_number(region)
    if not example:
        status("Aucun exemple disponible pour ce pays.", "warn")
    else:
        console.print(Panel(f"[bold bright_cyan]{phonenumbers.format_number(example, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}[/bold bright_cyan]\n[grey62]Numéro d'exemple documentaire — ne pas supposer qu'il est attribué ou joignable.[/grey62]", title="EXEMPLE", border_style="bright_cyan"))
    wait()


def phone_mask():
    title("PHONE • MASQUAGE", "Masquer les chiffres sensibles avant partage")
    raw=ask("Numéro à masquer")
    if not raw:
        wait(); return
    digits="".join(c for c in raw if c.isdigit())
    if len(digits) < 4:
        status("Numéro trop court pour être masqué correctement.", "warn")
    else:
        masked="•" * max(0, len(digits)-4) + digits[-4:]
        console.print(Panel(f"Entrée : {raw}\nMasqué : {masked}\n[grey62]Seuls les quatre derniers chiffres sont conservés.[/grey62]", title="RÉSULTAT", border_style="bright_magenta"))
        if confirm("Copier le résultat dans le presse-papiers ?", default=False):
            try:
                import tkinter as tk
                root=tk.Tk(); root.withdraw(); root.clipboard_clear(); root.clipboard_append(masked); root.update(); root.destroy()
                status("Résultat copié.", "ok")
            except Exception:
                status("Presse-papiers indisponible sur ce système.", "warn")
    wait()


def phone_link_generator():
    title("PHONE • LIENS", "Créer des liens d'appel ou WhatsApp Click-to-Chat")
    raw=ask("Numéro avec indicatif international conseillé")
    if not raw:
        wait(); return
    digits="".join(c for c in raw if c.isdigit())
    if len(digits)<7 or len(digits)>15:
        status("Longueur inhabituelle. Vérifie le numéro et son indicatif.", "warn")
    tel="tel:+"+digits
    wa="https://wa.me/"+digits
    console.print(Panel(f"Lien d'appel : [underline]{tel}[/underline]\nLien WhatsApp : [underline]{wa}[/underline]\n[grey62]Le lien WhatsApp n'envoie rien automatiquement et ne confirme pas que le numéro utilise WhatsApp.[/grey62]", title="LIENS GÉNÉRÉS", border_style="bright_cyan"))
    if confirm("Ouvrir le lien WhatsApp dans le navigateur ?", default=False):
        webbrowser.open(wa)
    wait()


def phone_vcard_export():
    title("PHONE • CONTACT VCARD", "Créer une fiche contact locale .vcf")
    name=ask("Nom du contact")
    raw=ask("Numéro de téléphone")
    if not name or not raw:
        status("Le nom et le numéro sont nécessaires.", "warn"); wait(); return
    lib, parsed = _parse_phone(raw, ask("Pays par défaut", "FR"))
    if not lib or not parsed:
        wait(); return
    number=lib.format_number(parsed, lib.PhoneNumberFormat.INTERNATIONAL)
    safe_name=re.sub(r"[^\w.-]+", "_", name, flags=re.UNICODE).strip("_.") or "contact"
    path=REPORTS_DIR / f"contact_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.vcf"
    escaped_name=name.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", " ")
    escaped_number=number.replace(";", "\\;").replace(",", "\\,")
    path.write_text(f"BEGIN:VCARD\nVERSION:3.0\nFN:{escaped_name}\nTEL;TYPE=CELL:{escaped_number}\nEND:VCARD\n", encoding="utf-8")
    status(f"Fiche contact créée localement : {path.name}", "ok")
    console.print("[grey62]Le fichier contient les informations que tu as saisies. Garde-le privé si nécessaire.[/grey62]")
    wait()


def phone_spam_search():
    title("PHONE • SIGNALEMENTS PUBLICS", "Rechercher des signalements publics de spam ou d'arnaque")
    raw=ask("Numéro à rechercher")
    if not raw:
        wait(); return
    query=urllib.parse.quote_plus(f'"{raw}" (spam OR arnaque OR démarchage OR scam)')
    url="https://www.google.com/search?q="+query
    console.print(Panel("Cette recherche vise les signalements publics. Elle ne permet pas d'identifier de façon fiable un particulier ni de confirmer qui appelle.", title="CONFIDENTIALITÉ", border_style="yellow"))
    open_link(url)
    wait()


def phone_compare():
    title("PHONE • COMPARATEUR", "Comparer deux numéros selon les métadonnées locales")
    a=ask("Premier numéro")
    b=ask("Deuxième numéro")
    region=ask("Pays par défaut", "FR").upper()
    if not a or not b:
        wait(); return
    lib, pa=_parse_phone(a, region)
    if not lib or not pa:
        wait(); return
    lib2, pb=_parse_phone(b, region)
    if not lib2 or not pb:
        wait(); return
    fmt=lib.PhoneNumberFormat.INTERNATIONAL
    rows=[("Numéro A", lib.format_number(pa,fmt)), ("Numéro B", lib.format_number(pb,fmt)), ("Même numéro normalisé", "Oui" if lib.is_number_match(pa,pb)==lib.MatchType.EXACT_MATCH else "Non"), ("Même indicatif pays", "Oui" if pa.country_code==pb.country_code else "Non"), ("Pays/région A", lib.region_code_for_number(pa) or "Inconnu"), ("Pays/région B", lib.region_code_for_number(pb) or "Inconnu")]
    table=make_table("COMPARAISON", ["Champ", "Résultat"])
    for row in rows: table.add_row(*row)
    console.print(table)
    wait()


def phone_extension_notes():
    title("PHONE • FORMAT / EXTENSION", "Préparer un numéro avec poste interne")
    raw=ask("Numéro principal")
    ext=ask("Poste interne (chiffres uniquement)")
    if not raw:
        wait(); return
    region=ask("Pays par défaut", "FR")
    lib, parsed=_parse_phone(raw, region)
    if not lib or not parsed:
        wait(); return
    if ext and not ext.isdigit():
        status("Le poste doit contenir uniquement des chiffres.", "error"); wait(); return
    parsed.extension=ext
    international=lib.format_number(parsed, lib.PhoneNumberFormat.INTERNATIONAL)
    rfc=lib.format_number(parsed, lib.PhoneNumberFormat.RFC3966)
    console.print(Panel(f"International : {international}\nLien RFC3966 : {rfc}", title="RÉSULTAT", border_style="bright_cyan"))
    wait()


def phone_metadata_report():
    title("PHONE • RAPPORT TECHNIQUE", "Résumé local de métadonnées sans recherche d'identité")
    raw=ask("Numéro à analyser")
    if not raw:
        wait(); return
    region=ask("Pays par défaut", "FR")
    lib, parsed=_parse_phone(raw, region)
    if not lib or not parsed:
        wait(); return
    carrier=__import__("phonenumbers.carrier", fromlist=["name_for_number"])
    geocoder=__import__("phonenumbers.geocoder", fromlist=["description_for_number"])
    tz=__import__("phonenumbers.timezone", fromlist=["time_zones_for_number"])
    data={"international":lib.format_number(parsed,lib.PhoneNumberFormat.INTERNATIONAL),"e164":lib.format_number(parsed,lib.PhoneNumberFormat.E164),"possible":lib.is_possible_number(parsed),"valid_by_metadata":lib.is_valid_number(parsed),"region_code":lib.region_code_for_number(parsed),"country_description":geocoder.description_for_number(parsed,"fr") or "Non disponible","carrier_metadata":carrier.name_for_number(parsed,"fr") or "Non disponible","time_zones":list(tz.time_zones_for_number(parsed)),"note":"Les métadonnées ne donnent ni le titulaire ni sa localisation en temps réel."}
    table=make_table("RAPPORT MÉTADONNÉES", ["Champ", "Résultat"])
    for key,value in data.items(): table.add_row(key, ", ".join(value) if isinstance(value,list) else str(value))
    console.print(table)
    maybe_save("phone_metadata_report", data)
    wait()


# ---------------- OUTILS SUPPLÉMENTAIRES ----------------

def system_info():
    title("System Information", "Informations locales sur la machine")
    rows = [
        ("Système", platform.system()),
        ("Version", platform.version()),
        ("Machine", platform.machine()),
        ("Processeur", platform.processor() or "Non renseigné"),
        ("Cœurs logiques", os.cpu_count()),
        ("Nom de l'hôte", socket.gethostname()),
        ("Python", sys.version.split()[0]),
        ("Heure locale", datetime.now().astimezone().isoformat(timespec="seconds")),
    ]
    try:
        import psutil
        mem = psutil.virtual_memory()
        rows.extend([("RAM totale", f"{mem.total / 1024**3:.2f} Go"), ("RAM utilisée", f"{mem.percent}%")])
    except ImportError:
        rows.append(("RAM", "Installe psutil pour les statistiques mémoire"))
    table = make_table("SYSTEM OVERVIEW", ["Champ", "Valeur"])
    for k, v in rows:
        table.add_row(str(k), str(v))
    console.print(table)
    maybe_save("system_info", dict(rows))
    wait()

def local_interfaces():
    title("Local Network Interfaces", "Adresses réseau de cette machine")
    table = make_table("NETWORK INTERFACES", ["Interface", "Adresse", "Famille"])
    try:
        import psutil
        for name, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                if addr.family in (socket.AF_INET, socket.AF_INET6):
                    table.add_row(name, addr.address, "IPv4" if addr.family == socket.AF_INET else "IPv6")
    except ImportError:
        try:
            table.add_row(socket.gethostname(), socket.gethostbyname(socket.gethostname()), "IPv4")
        except OSError as error:
            table.add_row("Erreur", str(error), "—")
        status("Installe psutil pour afficher toutes les interfaces.", "warn")
    console.print(table)
    wait()

def password_generator():
    title("Password Generator", "Génération locale avec secrets")
    raw = ask("Longueur (8 à 128)", "24")
    if not raw.isdigit() or not 8 <= int(raw) <= 128:
        status("La longueur doit être comprise entre 8 et 128.", "error")
        wait()
        return
    length = int(raw)
    alphabet = string.ascii_letters + string.digits + "!@#$%&*+-_?"
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    console.print(Panel(Text(password, style="bold bright_green"), title="MOT DE PASSE GÉNÉRÉ", border_style="bright_magenta"))
    console.print("[grey62]Garde-le privé et stocke-le dans un gestionnaire de mots de passe.[/grey62]")
    if confirm("Enregistrer l'empreinte du résultat (pas le mot de passe) dans un rapport ?"):
        save_report("password_generated", {"length": length, "sha256": hashlib.sha256(password.encode()).hexdigest()})
    wait()

def text_hash():
    title("SHA-256 Text", "Calcul local d'une empreinte")
    value = ask("Texte à hacher")
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    console.print(Panel(digest, title="SHA-256", border_style="bright_cyan"))
    maybe_save("text_sha256", {"sha256": digest, "text_length": len(value)})
    wait()

def base64_tool():
    title("Base64 Encoder / Decoder", "Encodage de texte, pas de chiffrement")
    mode = ask("1 = encoder  |  2 = décoder", "1")
    value = ask("Texte")
    try:
        if mode == "2":
            result = base64.b64decode(value.encode("ascii"), validate=True).decode("utf-8", errors="replace")
        else:
            result = base64.b64encode(value.encode("utf-8")).decode("ascii")
        console.print(Panel(Text(result, style="bold bright_green"), title="RÉSULTAT", border_style="bright_cyan"))
    except Exception as error:
        status(f"Impossible de traiter cette valeur : {error}", "error")
    wait()

def url_codec():
    title("URL Encoder / Decoder", "Encodage percent-encoding")
    mode = ask("1 = encoder  |  2 = décoder", "1")
    value = ask("Texte ou URL")
    result = urllib.parse.unquote(value) if mode == "2" else urllib.parse.quote(value, safe="")
    console.print(Panel(Text(result, style="bold bright_green"), title="RÉSULTAT", border_style="bright_cyan"))
    wait()

def json_formatter():
    title("JSON Formatter", "Validation et mise en forme")
    raw = ask("Colle le JSON sur une seule ligne")
    try:
        data = json.loads(raw)
        formatted = json.dumps(data, ensure_ascii=False, indent=2)
        console.print(Panel(Text(formatted), title="JSON VALIDE", border_style="bright_green"))
        if confirm("Enregistrer ce JSON formaté dans un fichier ?"):
            output = REPORTS_DIR / f"json_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            output.write_text(formatted, encoding="utf-8")
            status(f"Fichier créé : {output}", "ok")
    except json.JSONDecodeError as error:
        status(f"JSON invalide à la ligne {error.lineno}, colonne {error.colno} : {error.msg}", "error")
    wait()

def disk_usage():
    title("Disk Usage", "Espace disque disponible")
    raw = ask("Chemin à vérifier", str(Path.home()))
    try:
        usage = shutil.disk_usage(Path(raw).expanduser())
        rows = [("Chemin", raw), ("Total", f"{usage.total / 1024**3:.2f} Go"),
                ("Utilisé", f"{usage.used / 1024**3:.2f} Go"), ("Libre", f"{usage.free / 1024**3:.2f} Go"),
                ("Occupation", f"{usage.used / usage.total * 100:.1f}%")]
        table = make_table("DISK USAGE", ["Champ", "Valeur"])
        for k, v in rows: table.add_row(k, v)
        console.print(table)
    except Exception as error:
        status(str(error), "error")
    wait()

def folder_browser():
    title("Folder Browser", "Lister un dossier local")
    raw = ask("Chemin du dossier", str(Path.home())).strip('"')
    folder = Path(raw).expanduser()
    if not folder.is_dir():
        status("Dossier introuvable.", "error")
        wait()
        return
    table = make_table(f"CONTENU : {folder}", ["Type", "Nom", "Taille"])
    try:
        entries = sorted(folder.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for entry in entries[:150]:
            try:
                size = f"{entry.stat().st_size:,} octets" if entry.is_file() else "—"
            except OSError:
                size = "indisponible"
            table.add_row("Dossier" if entry.is_dir() else "Fichier", entry.name, size)
        console.print(table)
        if len(entries) > 150: status("Affichage limité aux 150 premiers éléments.", "warn")
    except OSError as error:
        status(str(error), "error")
    wait()

def timestamp_tool():
    title("Timestamp Converter", "Conversion d'un timestamp Unix")
    raw = ask("Timestamp Unix (laisser vide pour maintenant)")
    try:
        stamp = float(raw) if raw else time.time()
        local = datetime.fromtimestamp(stamp).astimezone()
        utc = datetime.fromtimestamp(stamp, timezone.utc)
        table = make_table("DATE CONVERSION", ["Format", "Valeur"])
        table.add_row("Timestamp", str(stamp))
        table.add_row("Local", local.isoformat(timespec="seconds"))
        table.add_row("UTC", utc.isoformat(timespec="seconds"))
        console.print(table)
    except (ValueError, OverflowError, OSError) as error:
        status(f"Timestamp invalide : {error}", "error")
    wait()

def calculator():
    title("Calculator", "Calcul arithmétique simple")
    expr = ask("Expression (ex. 12*(3+4)/2)")
    if not expr or not all(ch in "0123456789.+-*/()% " for ch in expr):
        status("Expression vide ou caractères non autorisés.", "error")
        wait()
        return
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
           ast.USub: operator.neg, ast.UAdd: operator.pos}
    def evaluate(node):
        if isinstance(node, ast.Expression): return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)): return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops: return ops[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in ops: return ops[type(node.op)](evaluate(node.operand))
        raise ValueError("Expression non autorisée")
    try:
        result = evaluate(ast.parse(expr, mode="eval"))
        console.print(Panel(str(result), title="RÉSULTAT", border_style="bright_green"))
    except Exception as error:
        status(f"Calcul impossible : {error}", "error")
    wait()

def open_url_tool():
    title("Open URL", "Ouvrir une page dans le navigateur")
    url = ask("URL")
    if url:
        if not url.startswith(("https://", "http://")):
            url = "https://" + url
        if urllib.parse.urlparse(url).scheme in ("http", "https"):
            open_link(url)
        else:
            status("URL non valide.", "error")
    wait()

# ---------------- RAPPORTS ----------------

def report_center():
    title("Report Center", "Historique des rapports JSON")
    files = sorted(REPORTS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    table = make_table("RECENT REPORTS", ["Date", "Fichier", "Taille"])
    for path in files[:50]:
        modified = datetime.fromtimestamp(path.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
        table.add_row(modified, path.name, f"{path.stat().st_size:,} B")
    if not files:
        table.add_row("-", "Aucun rapport", "-")
    console.print(table)
    console.print(f"\n[grey62]Dossier :[/grey62] {REPORTS_DIR}")
    if confirm("Ouvrir le dossier des rapports ?"):
        try:
            if os.name == "nt":
                os.startfile(str(REPORTS_DIR))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(REPORTS_DIR)])
            else:
                subprocess.Popen(["xdg-open", str(REPORTS_DIR)])
        except Exception as error:
            status(str(error), "error")
    wait()

# ---------------- MENU PRINCIPAL ----------------


def command_help():
    title("Aide des commandes", "Choisis un numéro pour comprendre son utilité, ses entrées et ses limites")
    descriptions = {
        "01": ("Recherche par pseudo", "Ouvre des recherches publiques d'un pseudo sur plusieurs moteurs et plateformes. Les correspondances doivent être vérifiées manuellement."),
        "02": ("Recherche nom / prénom", "Prépare des recherches web publiques sur un nom ou prénom. Un homonyme n'est pas une preuve d'identité."),
        "03": ("Analyse d'e-mail", "Vérifie la syntaxe et tente de lire les enregistrements MX du domaine. Cela ne confirme pas que la boîte existe."),
        "04": ("Recherche TikTok", "Ouvre une recherche TikTok publique par pseudo ou mots-clés."),
        "05": ("Empreinte de domaine", "Normalise un domaine, interroge quelques types DNS si dnspython est installé et propose des sources publiques RDAP, crt.sh et URLScan."),
        "06": ("Recherche approfondie de pseudo", "Prépare des liens de recherche sur des plateformes publiques. Un pseudo identique ne prouve pas que les comptes sont liés."),
        "07": ("Réputation d'URL", "Ouvre des sources publiques pour rechercher des signalements. SYNERGIE ne visite pas automatiquement l'URL et ne garantit pas un verdict."),
        "08": ("Constructeur de recherche web", "Compose une requête avec mots-clés, site:, expression exacte et filetype:. À utiliser uniquement pour des informations publiques autorisées."),
        "09": ("Ressources d'exposition d'e-mail", "Fournit des sites où vérifier manuellement sa propre adresse et des recherches publiques. Aucune base de fuites n'est interrogée automatiquement."),
        "10": ("Recherche inversée d'image", "Ouvre Google Lens, Bing Visual Search et TinEye. Tu choisis manuellement si tu téléverses l'image."),
        "11": ("Recherche sociale publique", "Prépare une recherche par mot-clé sur moteurs, actualités et plateformes publiques."),
        "12": ("Métadonnées d'un fichier local", "Affiche nom, extension, taille, date de modification, SHA-256 et EXIF si Pillow est installé. Le chemin local peut être sensible."),
        "13": ("Recherche DNS", "Interroge les enregistrements DNS d'un domaine si dnspython est disponible."),
        "14": ("Informations IP / domaine", "Affiche des informations réseau publiques résolues pour une IP ou un domaine. La géolocalisation IP n'est jamais exacte à l'adresse."),
        "15": ("Test TCP hôte / port", "Teste si une connexion TCP vers un hôte et un port répond depuis ton ordinateur. Utilise-le uniquement sur des systèmes autorisés."),
        "16": ("Connectivité Discord", "Vérifie l'accès réseau à des points de service Discord."),
        "17": ("Diagnostics réseau", "Affiche des informations de connectivité utiles au dépannage local."),
        "18": ("Microsoft Defender", "Consulte ou lance les actions Defender prévues par l'outil sur Windows. Vérifie les confirmations avant toute action."),
        "19": ("Scan heuristique de dossier", "Recherche des indicateurs simples dans les fichiers d'un dossier. Ce n'est pas un antivirus et des faux positifs sont possibles."),
        "20": ("Audit statique Python", "Examine un script Python à la recherche de motifs potentiellement risqués sans l'exécuter."),
        "21": ("Calcul SHA-256 de fichier", "Calcule l'empreinte SHA-256 d'un fichier pour vérifier son intégrité."),
        "22": ("Analyse de fichier", "Affiche des informations générales sur un fichier choisi localement."),
        "23": ("OSINT Discord", "Analyse les informations calculables depuis un ID et ouvre des recherches publiques de pseudo. Ne révèle pas de données privées."),
        "24": ("Générateur de timestamps Discord", "Convertit une date/heure en timestamp Discord et montre les formats d'affichage."),
        "25": ("Constructeur de lien de message Discord", "Construit un lien de message à partir des IDs du serveur, du salon et du message."),
        "26": ("Invitations Discord", "Ouvre ou prépare un lien d'invitation fourni par l'utilisateur."),
        "27": ("Liens publics d'un profil Discord", "Prépare les liens de profil ou de recherche associés à un ID/pseudo."),
        "28": ("Lecteur de permissions Discord", "Interprète une valeur numérique de permissions Discord selon les drapeaux pris en charge."),
        "29": ("Ressources Discord", "Ouvre les ressources officielles et la page d'état de Discord."),
        "30": ("Aide Markdown Discord", "Montre des exemples de mise en forme des messages Discord."),
        "31": ("Webhook Discord", "Envoie un message via une URL de webhook fournie. Garde l'URL secrète et vérifie le salon avant d'envoyer."),
        "32": ("Assistant de création de bot Discord", "Génère un projet de bot avec commandes. Il faut créer l'application, configurer le token localement et accorder seulement les permissions nécessaires."),
        "33": ("Analyse complète d'un numéro", "Analyse le format et les métadonnées publiques disponibles via la bibliothèque phonenumbers. Ne donne pas l'identité ni la position du titulaire."),
        "34": ("Convertisseur de formats téléphone", "Convertit un numéro entre formats nationaux et internationaux lorsque la région est connue."),
        "35": ("Validation par lot", "Vérifie le format de plusieurs numéros fournis. La validité de format ne prouve pas que les lignes sont actives."),
        "36": ("Référence des indicatifs pays", "Aide à retrouver les indicatifs téléphoniques internationaux."),
        "37": ("Générateur de numéro d'exemple", "Produit un exemple de numéro pour les tests, pas un numéro attribué garanti."),
        "38": ("Masquage de numéro", "Masque une partie d'un numéro avant de l'afficher ou de le partager."),
        "39": ("Liens tel: et WhatsApp", "Crée un lien d'appel ou un lien WhatsApp à partir d'un numéro fourni."),
        "40": ("Export vCard", "Crée une fiche contact au format vCard à partir des informations saisies."),
        "41": ("Recherche de signalements spam", "Prépare des recherches publiques de signalements. Les résultats peuvent être inexacts ou manipulés."),
        "42": ("Comparer deux numéros", "Compare les versions normalisées de deux numéros selon la région indiquée."),
        "43": ("Formater un poste interne", "Présente un numéro avec une extension ou un poste interne."),
        "44": ("Rapport de métadonnées téléphone", "Produit un rapport technique de format et métadonnées disponibles, sans révéler l'identité du titulaire."),
        "45": ("Centre de rapports", "Consulte les rapports JSON sauvegardés par SYNERGIE."),
        "46": ("Informations du PC", "Affiche des informations système générales sur l'ordinateur local."),
        "47": ("Interfaces réseau locales", "Liste les interfaces et adresses réseau locales accessibles."),
        "48": ("Espace disque", "Affiche l'espace total, utilisé et libre des volumes détectés."),
        "49": ("Explorateur de dossiers", "Permet de parcourir des dossiers locaux."),
        "50": ("Convertisseur timestamp", "Convertit un timestamp Unix en date lisible ou l'inverse."),
        "51": ("Calculatrice sécurisée", "Évalue des expressions mathématiques simples avec une liste d'opérations autorisées."),
        "52": ("Ouvrir une URL", "Ouvre une URL dans le navigateur après confirmation. Vérifie le domaine avant d'ouvrir."),
        "53": ("Générateur de mot de passe", "Génère un mot de passe aléatoire avec les caractères sélectionnés."),
        "54": ("SHA-256 d'un texte", "Calcule l'empreinte SHA-256 d'un texte saisi."),
        "55": ("Base64", "Encode ou décode du texte en Base64. Base64 n'est pas un chiffrement."),
        "56": ("Encodeur / décodeur URL", "Encode ou décode des caractères pour une URL."),
        "57": ("Formateur JSON", "Valide et met en forme du JSON pour le rendre lisible."),
        "58": ("Aide des commandes", "Affiche la description d'une option numérotée. Saisis le numéro, par exemple 32 pour le générateur de bot Discord."),
    }
    number = ask("Numéro de commande à expliquer (01–58)", "32")
    number = number.strip().zfill(2) if number.strip().isdigit() else number.strip()
    item = descriptions.get(number)
    if not item:
        status("Numéro inconnu. Choisis une option de 01 à 58.", "error")
        wait()
        return
    name, description = item
    console.print(Panel(
        f"[bold bright_cyan]Option {number} — {name}[/bold bright_cyan]\n\n{description}",
        title="EXPLICATION DE LA COMMANDE",
        border_style="bright_magenta",
        box=box.ROUNDED,
    ))
    wait()


def main():
    # Options rangées par catégorie : OSINT, réseau, sécurité, Discord, téléphone,
    # système, puis utilitaires. L'option 58 explique n'importe quelle commande.
    actions = {
        "01": username_search,
        "02": name_search,
        "03": email_osint,
        "04": tiktok_search,
        "05": domain_osint,
        "06": username_deep_search,
        "07": url_reputation_lookup,
        "08": public_query_builder,
        "09": email_exposure_resources,
        "10": reverse_image_search,
        "11": public_social_search,
        "12": local_file_metadata,
        "13": dns_lookup,
        "14": ip_lookup,
        "15": tcp_test,
        "16": discord_connection_test,
        "17": network_diagnostics,
        "18": defender,
        "19": folder_scan,
        "20": source_audit,
        "21": hash_file,
        "22": analyze_file,
        "23": discord_osint,
        "24": discord_timestamp,
        "25": discord_message_link,
        "26": discord_invite,
        "27": discord_profile_links,
        "28": discord_permissions,
        "29": discord_resources,
        "30": discord_markdown,
        "31": discord_webhook_sender,
        "32": discord_bot_builder,
        "33": phone_lookup,
        "34": phone_format_converter,
        "35": phone_batch_validate,
        "36": phone_country_reference,
        "37": phone_example_generator,
        "38": phone_mask,
        "39": phone_link_generator,
        "40": phone_vcard_export,
        "41": phone_spam_search,
        "42": phone_compare,
        "43": phone_extension_notes,
        "44": phone_metadata_report,
        "45": report_center,
        "46": system_info,
        "47": local_interfaces,
        "48": disk_usage,
        "49": folder_browser,
        "50": timestamp_tool,
        "51": calculator,
        "52": open_url_tool,
        "53": password_generator,
        "54": text_hash,
        "55": base64_tool,
        "56": url_codec,
        "57": json_formatter,
        "58": command_help,
    }

    startup_animation()
    while True:
        dashboard()
        show_menu("01–12 / OSINT PUBLIC", [
            ("01", "Recherche par pseudo"),
            ("02", "Recherche nom / prénom"),
            ("03", "Analyse d'adresse e-mail"),
            ("04", "Recherche TikTok publique"),
            ("05", "Empreinte de domaine / DNS / RDAP"),
            ("06", "Recherche approfondie de pseudo"),
            ("07", "Sources de réputation d'URL"),
            ("08", "Constructeur de recherche web"),
            ("09", "Ressources de vérification d'e-mail"),
            ("10", "Recherche inversée d'image"),
            ("11", "Recherche sociale publique"),
            ("12", "Métadonnées et SHA-256 d'un fichier local"),
        ])
        show_menu("13–17 / NETWORK", [
            ("13", "Recherche DNS"),
            ("14", "Informations IP / domaine"),
            ("15", "Test TCP hôte / port"),
            ("16", "Connectivité Discord"),
            ("17", "Diagnostics réseau"),
        ])
        show_menu("18–22 / PC SECURITY", [
            ("18", "Microsoft Defender"),
            ("19", "Scan heuristique de dossier"),
            ("20", "Audit statique Python"),
            ("21", "Calcul SHA256 de fichier"),
            ("22", "Analyse de fichier"),
        ], border="medium_purple")
        show_menu("23–32 / DISCORD", [
            ("23", "OSINT public / analyse d'ID / pseudo"),
            ("24", "Générateur de timestamps"),
            ("25", "Constructeur de lien de message"),
            ("26", "Ouvrir / préparer une invitation"),
            ("27", "Liens publics d'un profil"),
            ("28", "Lecteur de permissions"),
            ("29", "Ressources et statut officiels"),
            ("30", "Aide Markdown"),
            ("31", "Envoyer un message via webhook"),
            ("32", "Assistant guidé : générer un bot Discord"),
        ], border="bright_blue")
        show_menu("33–44 / NUMÉRO DE TÉLÉPHONE", [
            ("33", "Analyse complète du numéro"),
            ("34", "Convertisseur de formats"),
            ("35", "Validation par lot"),
            ("36", "Référence des indicatifs pays"),
            ("37", "Générateur de numéro d'exemple"),
            ("38", "Masquer un numéro"),
            ("39", "Créer liens tel: et WhatsApp"),
            ("40", "Exporter une fiche contact vCard"),
            ("41", "Recherche de signalements publics spam/arnaque"),
            ("42", "Comparer deux numéros normalisés"),
            ("43", "Formater un numéro avec poste interne"),
            ("44", "Rapport technique de métadonnées"),
        ], border="bright_magenta")
        show_menu("45–52 / SYSTEM & UTILITIES", [
            ("45", "Centre / historique des rapports"),
            ("46", "Informations du PC"),
            ("47", "Interfaces réseau locales"),
            ("48", "Espace disque"),
            ("49", "Explorateur de dossiers"),
            ("50", "Convertisseur timestamp"),
            ("51", "Calculatrice sécurisée"),
            ("52", "Ouvrir une URL"),
        ], border="grey50")
        show_menu("53–57 / CRYPTO & TEXT", [
            ("53", "Générateur de mot de passe"),
            ("54", "SHA-256 d'un texte"),
            ("55", "Encodeur / décodeur Base64"),
            ("56", "Encodeur / décodeur URL"),
            ("57", "Formateur JSON"),
        ], border="bright_cyan")
        show_menu("58 / AIDE", [
            ("58", "À quoi sert une commande ? Explication détaillée par numéro"),
            ("00", "Quitter"),
        ], border="bright_yellow")

        choice = ask("SYNERGIE — numéro (01–58, 58 = aide, 00 = quitter)", "00")
        normalized = choice.strip()
        if normalized.lower() in ("0", "00", "q", "quit", "exit"):
            clear()
            console.print(Panel(
                Align.center(Text("SYNERGIE\nSession terminée.", style="bold bright_cyan", justify="center")),
                border_style="bright_cyan",
                box=box.DOUBLE,
            ))
            break
        if normalized.isdigit():
            normalized = normalized.zfill(2)
        action = actions.get(normalized)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                status("Opération interrompue.", "warn")
                wait()
            except Exception as error:
                status(f"Erreur inattendue : {error}", "error")
                wait()
        else:
            status("Option inconnue. Choisis un numéro entre 01 et 58.", "warn")
            wait()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bright_yellow]Fermeture de SYNERGIE MULTITOOL.[/bright_yellow]")
