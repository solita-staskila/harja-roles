## harja-roles
roles parser

<br>

## Requirements 
- [Python & Pip](https://github.com/solita-staskila/harja-roles?tab=readme-ov-file#ajo-linuxmac) 
- [wkhtmltopdf](https://github.com/solita-staskila/harja-roles?tab=readme-ov-file#ajo-linuxmac)

<br>

## Ajo (Linux/Mac)
- **git clone** tai lataa repo 
- Avaa terminaali (root directory)
- Asenna systeemin depsut:
```
sudo apt-get update
sudo apt install python3
sudo apt-get -y install wkhtmltopdf
sudo apt install python3-pip
sudo apt install virtualenv
```
<br>

- Tee python venv (virtual environment):
```
python3 -m virtualenv venv
```
<br>

- Aktivoi virtualenv:
```
source venv/bin/activate 
```

> Virtualenv luo erillisen Python-ympäristön, jossa projektin omat kirjastot pysyvät erillään muista projekteista
>
> Kaikki python depsut asennetaan lokaalisti .venv kansioon 
<br>

- Asenna python depsut:
```
pip install -r requirements.txt 
```
<br>

- [Lataa data täältä](https://extranet.vayla.fi/wiki/pages/viewpage.action?pageId=221891359), heitä se root directoryyn

  Pitäisi näyttää tältä:
```
harja-roles/
├── data/
├── resources/
├── __init.py
```

<br>

## Run the script:
```
python __init.py --m
```
#### Tai:
```
python __init.py --m --v
```
#### Tai:
```
python __init.py --help 
```

<br>

### Seuraavat raportit generoidaan:
```
./report.pdf
./report.html
```
