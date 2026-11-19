# messages: the wording of everything the app shows

Every message the user sees is a key in an ARB file, as Flutter does it (https://docs.flutter.dev/ui/internationalization). The requirements never contain the wording; they cite the key.

- `app_en.arb` is the template. It defines every key, with its English text. A text with `{name}` has that placeholder, listed in the key's `@key` entry.
- `app_es.arb`, `app_fr.arb`, `app_de.arb`, `app_pt.arb` and `app_nl.arb` have the same keys with their translations. A language with no translation of a key falls back to English.
- A requirement that shows a message cites its key as `msg:key` and says when it is shown and what each placeholder holds. Nothing else about the wording is said in the requirement.
- To change a wording, change it here. No requirement changes.

Keys were made from the old app's English texts (first words, camel case), and the translations are the old app's. 91 of the English texts still carry HTML markup from the old pages; a requirement that cites one replaces the markup with a plain message, or says which parts are emphasized. The keys are not final names: renaming one is a change to every locale file and to the rows that cite it.
