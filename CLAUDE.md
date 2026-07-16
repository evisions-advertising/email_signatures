# evisions – Emailové podpisy

Tento repozitář je **jediný zdroj pravdy** pro e-mailové podpisy zaměstnanců evisions.cz.
Live náhled (GitHub Pages): https://evisions-advertising.github.io/email_signatures/

## Struktura

```
photos/                 profilové fotky, <slug>.png (slug = část e-mailu před @, ASCII bez diakritiky)
signatures/<TÝM>/       HTML podpisy dle týmů (AI, KREA, Management, Office, PPC, SCS, SEO, UX)
template.html           kanonická šablona pro nové podpisy
people.csv              evidence lidí (jméno, tým, interně/externě, e-mail, telefon, fotka)
index.html              náhledová stránka s Copy tlačítky – NIKDY needitovat ručně, vždy generovat
scripts/generate_preview.py  generátor index.html
```

## Klíčová pravidla

1. **Slug** = část e-mailu před `@`, malými písmeny, bez diakritiky (broz@evisions.cz → `broz`).
   Slug určuje název fotky (`photos/broz.png`) i URL v podpisu.
2. **Profilová fotka** se odkazuje VŽDY přes
   `https://raw.githubusercontent.com/evisions-advertising/email_signatures/main/photos/<slug>.png`
3. **Logo, ikony soc. sítí a oddělovací linka zůstávají na Imguru** – neměnit:
   logo `Na7CmmQ`, Instagram `oE0aJGv`, Facebook `52cHgsW`, LinkedIn `cDYdXrV`, linka `l1UCnKV`.
4. Instagram odkaz je `https://www.instagram.com/evisions_cz` (NE evisions_advertising).
5. **line-height musí být explicitní** (18px jméno, 16px pozice a kontakty) – jinak Gmail rozhodí řádkování.
6. „Job Title" zůstává jako placeholder – pozici si lidé doplňují sami.
7. Neznámý telefon = `+420 000 000 000` (lidé si doplní sami).
8. Šířka podpisu 338 px, font Arial, oranžová #F37021 – neměnit.
9. Po KAŽDÉ změně v `signatures/` přegenerovat `index.html` skriptem a VŠE commitnout a pushnout
   (fotky + podpis + people.csv + index.html v jednom commitu).
10. **Automatický režim (autorizováno uživatelem):** u požadavků typu „nový zaměstnanec",
    „odchod zaměstnance" a „změna jména/fotky/týmu" proveď VŠECHNY kroky procesu a rovnou
    pushni (resp. commitni + mergni/pushni) přímo do `main` – BEZ čekání na potvrzení uživatele.
    Cílem je, aby změna byla live na GitHub Pages během ~1 minuty od zadání. Toto explicitní
    svolení se vztahuje na běžný, striktně dle procesu níže provedený zápis. Pokud narazíš na
    něco mimo proces (neobvyklý vstup, kolize slugu, chybějící fotka, nejasné jméno/tým), i tak
    se zeptej – automatizace platí pro provedení kroků, ne pro domýšlení nejasného zadání.
11. **Nasazení na Pages musí být spolehlivé:** push přes lokální git proxy tohoto sandboxu
    se na `main` propíše správně, ale nemusí spolehlivě odpálit GitHubí
    `pages-build-deployment` (workflow `dynamic/pages/pages-build-deployment`, nelze spustit
    ručně přes workflow_dispatch – vrací 422). Po pushi na `main` proto vždy ověř přes
    `mcp__github__actions_list` (`list_workflow_runs`, `resource_id` = ID workflow
    `pages-build-deployment`), že nový run odpovídá aktuálnímu `head_sha` z `main`. Pokud ne,
    „nudni" build reálným commitem přes GitHub API (`mcp__github__create_or_update_file`,
    např. no-op update `README.md`) – to build spolehlivě spustí. Sleduj run přes
    `actions_get` (`get_workflow_run`), dokud `status` není `completed` a `conclusion`
    `success`, než změnu nahlásíš jako live.

## Proces: nový zaměstnanec (uživatel pošle fotku + jméno)

Vstup: fotka v chatu, celé jméno, tým, volitelně telefon a interně/externě.

1. Odvoď slug z příjmení (bez diakritiky, malými písmeny). E-mail = `<slug>@evisions.cz`.
   Pokud si nejsi jistý (dvojí příjmení, kolize), zeptej se.
2. Ulož fotku jako `photos/<slug>.png` (ideálně kruhový ořez 350×350 jako ostatní; pokud
   fotka není v tomto formátu, upozorni uživatele, ale ulož ji).
3. Vytvoř `signatures/<TÝM>/email_signature-<Prijmeni>.html` z `template.html`:
   nahraď `{{JMENO}}`, `{{SLUG}}`, `{{TELEFON}}` (zobrazený formát s mezerami),
   `{{TELEFON_RAW}}` (bez mezer, s +420…).
4. Přidej řádek do `people.csv`.
5. Spusť `python scripts/generate_preview.py` (z kořene repa).
6. Commit + push. Ověř, že `https://raw.githubusercontent.com/.../photos/<slug>.png` vrací 200.

## Proces: odchod zaměstnance

1. Smaž `signatures/<TÝM>/email_signature-<Prijmeni>.html` a `photos/<slug>.png`.
2. Odeber řádek z `people.csv`.
3. Přegeneruj index.html, commit + push.
(Archiv bývalých podpisů se drží mimo GitHub, na firemním Disku ve složce `Outs`.)

## Proces: změna jména / fotky / týmu

- **Fotka:** nahraď `photos/<slug>.png` (stejný název!), commit + push. Podpisy se aktualizují samy.
- **Jméno (svatba apod.):** uprav jméno v HTML (jméno + `<title>`), pokud se mění e-mail,
  přejmenuj i fotku a soubor podpisu. Aktualizuj people.csv, přegeneruj, push.
- **Tým:** přesuň HTML do správné složky v `signatures/`, uprav people.csv, přegeneruj, push.

## Kontrola kvality (před každým pushem)

- [ ] jméno v podpisu i v `<title>` souboru
- [ ] fotka na GitHub raw URL se slugem dle e-mailu
- [ ] line-height 18/16/16 přítomné
- [ ] Instagram = evisions_cz
- [ ] index.html přegenerovaný skriptem (počet podpisů v H1 sedí)
- [ ] people.csv aktuální
