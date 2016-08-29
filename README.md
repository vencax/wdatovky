# wdatovky (web) datovky

posilac datovych zprav pres web easy peasy ... [https://wdatovky.herokuapp.com/](https://wdatovky.herokuapp.com/)

## API

Jedina POST routa s url [/api](https://wdatovky.herokuapp.com/api).
Umi POUZE application/json content type s nasledujicim schematem:
- recpt: adresa prijemce
- subj: predmet zpravy
- text: (optional) text zpravy - je zabalen jako plain/text priloha
- uname: uzivatelske jmeno pro DS
- pwd: heslo pro DS
- attach: (optional) pole objektu s 3 povinnymi atributy:
  - content_type: typ prilohy
  - filename: nazev prilohy
  - content: base64 zakodovany obsah prilohy

Priklad:

```
{
  'recpt': 'necocosivygooglim',
  'subj': 'pokusna zprava',
  'text': 'pozor, probiha pokus',
  'uname': 'fdjfls',
  'pwd': 'verySeccret',
  'attach': [{
    'content_type': 'image/png',
    'filename': 'jehehe.png',
    'content' 'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyEAYAAABOr1TyA...'
  }]
}
```


## For techs

Pouziva SOAP based kanal datovych schranek.
Toto je jen jednoduchy Flask based web server s formularem :)
Vic na:

- http://www.vxk.cz/blog/2013/03/21/datove-schranky-jinak/
- https://github.com/vencax/PyDatoveSchrankyBinarky
- https://github.com/vencax/dslib
