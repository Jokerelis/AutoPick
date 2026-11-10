# AutoPick – automobilių nuomos ir rezervacijų sistema

**AutoPick** – universiteto programų sistemų projektavimo kursinio darbo prototipas. Sistema leidžia peržiūrėti nuomojamus automobilius, kurti rezervacijas, patikrinti užimtumą, automatiškai apskaičiuoti kainą ir, kilus rezervacijos konfliktui, pasiūlyti alternatyvų automobilį. Alternatyvų eiliškumui gali būti naudojamas OpenAI modelis.

Projektą sudaro **React + Vite** naudotojo sąsaja, **Python + FastAPI** REST API, atskiras verslo logikos sluoksnis ir **SQLite** duomenų bazė. Duomenims pasiekti naudojama **SQLAlchemy**, o automatiniams testams – **pytest**.

## Pagrindinis principas – dvi nepriklausomos įmonės

Sistemoje yra du demonstraciniai klientai (angl. *tenants*): **Vilniaus** ir **Kauno** automobilių nuomos įmonės. Kiekviena įmonė turi savo automobilius ir rezervacijas.

- Įmonės identifikatorius (`company_id`) saugomas automobilių ir rezervacijų įrašuose.
- API užklausose pateikiamas `X-API-Key` raktas, kuris serverio pusėje susiejamas su konkrečia įmone.
- `app/auth.py` tikrina raktą ir teises; `app/main.py` bei verslo logikos užklausos riboja duomenis pagal įmonę.
- Vilniaus raktu negalima peržiūrėti ar rezervuoti Kauno automobilių, net pakeitus `company_id` URL adrese.
- Neautorizuota užklausa grąžina `401`, o bandymas naudotis kitos įmonės duomenimis – `403`.

**Apribojimas:** tai demonstracinis įmonių atskyrimas naudojant API raktus, o ne pilna naudotojų autentifikacija. Šioje versijoje nėra individualių paskyrų, slaptažodžių ar rolių. Raktas įvedamas React sąsajoje, todėl toks sprendimas skirtas tik vietiniam prototipo demonstravimui, ne viešam produkciniam diegimui.

## Pagrindinės funkcijos ir verslo taisyklės

1. **Rezervacija.** Klientas pasirenka automobilį, pradžios ir pabaigos datas, vairuotojo amžių bei vairavimo stažą. Pabaigos data turi būti vėlesnė už pradžios datą; praeities data negalima.
2. **Vairuotojo apribojimai.** Amžius – nuo 20 metų; vairavimo stažas – bent 1 metai.
3. **Užimtumo patikra.** Tikrinama, ar automobilis turi `Available` būseną ir ar pasirinktu laikotarpiu nėra persidengiančios `Confirmed` rezervacijos.
4. **Dinaminė kainodara.** Skaičiuojama bazinė dienos kaina, sezoniniai priedai, paklausos priedas, ilgalaikės nuomos nuolaida ir jauno vairuotojo priedas.
5. **Alternatyvos.** Kilus konfliktui, ieškoma iki 3 laisvų tos pačios įmonės ir kategorijos automobilių, kurių rezervacijos nesikerta su pasirinktomis datomis.
6. **AI rekomendacija.** Jei įjungtas OpenAI API, modelis iš **jau patikrintų alternatyvų** parenka tinkamiausią pagal pageidaujamą kėbulo tipą ir kainą. Python patikrina, ar grąžintas `car_id` tikrai yra leistinų alternatyvų sąraše. Jei AI nepasiekiamas arba atsakymas netinkamas, taikomas atsarginis algoritmas – rikiavimas pagal mažiausią bendrą kainą.

Kainodaros taisyklės:

| Sąlyga | Poveikis |
|---|---|
| Vairuotojas jaunesnis nei 25 metų | +15 % |
| Nuoma bent 7 dienoms | −10 % |
| Birželis–rugpjūtis: `Sport` arba `Convertible` | +15 % atitinkamoms dienoms |
| Gruodis–vasaris: `SUV` arba 4x4 | +15 % atitinkamoms dienoms |
| Tos pačios kategorijos užimtumas įmonėje ≥80 % | +10 % |

Nuomos dienų skaičius apskaičiuojamas neįtraukiant pabaigos datos. Taikymo seka: sezoninės dienų kainos, paklausos priedas, ilgos nuomos nuolaida, jauno vairuotojo priedas.
## Reikalingi įrankiai

- Windows, **Python 3.11+**, **Node.js 22.12+** ir npm.
- Internetas priklausomybėms įdiegti; tikroms AI rekomendacijoms reikia atskiro OpenAI API rakto.
- Python bibliotekos nurodytos `requirements.txt`, frontend versijos – `frontend/package.json`.

## Paruošimas (vieną kartą)

Projekto pagrindiniame kataloge vykdykite:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd frontend
npm install
cd ..
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m app.seed
```

`.env` faile įrašykite savo įmonių raktus ir, jei naudosite AI, OpenAI raktą:

```dotenv
AUTOPICK_VILNIUS_KEY=your-vilnius-key
AUTOPICK_KAUNAS_KEY=your-kaunas-key
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o-mini
AUTOPICK_AI_ENABLED=true
```

Be AI galima naudoti `AUTOPICK_AI_ENABLED=false`. **`.env` negalima kelti į GitHub.** SQLite duomenys laikomi vietiniame `autopick.db` faile.

## Paleidimas viena komanda

Po paruošimo, projekto pagrindiniame kataloge:

```powershell
.\start.bat
```

- **Svetainė:** http://localhost:5173
- **API dokumentacija:** http://127.0.0.1:8000/docs

`start.bat` atidaro FastAPI ir React serverius atskiruose terminaluose, o nesant DB ją sukuria. Serverius sustabdykite `Ctrl + C` jų languose.

## Demonstravimas

1. Paleiskite sistemą ir prisijunkite prie **Kauno** įmonės su jos API raktu.
2. Rezervuokite **Toyota Yaris** būsimoms datoms. Sistema parodys rezervacijos ID ir galutinę kainą.
3. Tomis pačiomis datomis rezervuokite Toyota Yaris dar kartą: gausite konfliktą (`409`) ir, jei laisvas, **Subaru Forester** alternatyvą. Bus parodyta `AI Recommendation` arba `Fallback Recommendation`.
4. Naudodami **Vilniaus** raktą, per API bandykite pasiekti `/companies/2/cars` – serveris turi grąžinti `403`.
5. Paleiskite automatinius testus.

## Demonstraciniai duomenys

| Įmonė (`company_id`) | Automobilis | Kategorija |
|---|---|---|
| Vilnius (`1`) | Volkswagen Golf | `Economic` |
| Vilnius (`1`) | Audi A6 | `Comfort` |
| Vilnius (`1`) | Mazda MX-5 | `Sport` |
| Vilnius (`1`) | BMW X5 | `Premium` |
| Kaunas (`2`) | Toyota Yaris | `Economic` |
| Kaunas (`2`) | BMW 320 | `Comfort` |
| Kaunas (`2`) | Subaru Forester | `Economic` |
| Kaunas (`2`) | BMW M4 | `Sport` |

Tai pradiniai `app/seed.py` duomenys. Vietiniai duomenų bazės pakeitimai ir rezervacijos išlieka tarp programos paleidimų.

## Testai

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

Testais tikrinamos kainodaros taisyklės, paklausos skaičiavimas, rezervacijos konfliktai bei alternatyvos ir įmonių duomenų izoliavimas. AI testams naudojami imituoti atsakymai, kad nereikėtų mokamų API užklausų. Faktinius sėkmingų testų rezultatus patikrinkite prieš atsiskaitymą.

## Projekto struktūra

- `app/main.py`, `auth.py` – FastAPI maršrutai ir prieigos kontrolė.
- `app/reservation_service.py` – rezervacijų kūrimas ir konfliktai.
- `app/pricing.py`, `demand.py` – dinaminė kainodara.
- `app/alternatives.py`, `ai_recommender.py` – alternatyvos ir AI rekomendacijos.
- `app/models.py`, `database.py`, `seed.py` – SQLite modeliai, prisijungimas ir pradiniai duomenys.
- `frontend/src/` – React sąsaja.
- `tests/` – automatiniai testai.

## Pakartotinis demonstracinių duomenų sukūrimas

**Dėmesio: šie veiksmai ištrina visas vietines rezervacijas ir kitus DB pakeitimus.** Sustabdykite FastAPI, tada vykdykite:

```powershell
Remove-Item .\autopick.db
.\.venv\Scripts\python.exe -m app.seed
```
