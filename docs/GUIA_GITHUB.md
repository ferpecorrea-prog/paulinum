# Guía paso a paso: subir paulinum_lab a GitHub (para quien nunca lo ha usado)

GitHub es un servicio gratuito que guarda carpetas de código con su historial de cambios y las hace
accesibles por un enlace. Se usa desde el navegador y, para subir carpetas enteras cómodamente, con la
aplicación gratuita **GitHub Desktop**. No hace falta escribir órdenes. Tiempo estimado: 30-40 minutos.

## Antes de empezar: qué se sube y qué no

Se sube la carpeta `paulinum_lab` entera **salvo** lo que excluye el archivo `.gitignore` que ya está en
ella: las descargas de textos (`data/raw/`), los corpus construidos (`data/cache/`) y las matrices grandes.
Esos archivos se regeneran con las órdenes del README y algunos no pueden redistribuirse por su licencia.
Todo lo demás (código, configuraciones, metadatos, resultados, informes, tablas publicadas, documentación)
sí se sube. GitHub admite archivos de hasta 100 MB; ninguno de los que se suben se acerca a ese límite.

## Paso 1. Crear una cuenta en GitHub

1. Entre en https://github.com y pulse **Sign up**.
2. Escriba su correo, elija una contraseña y un **nombre de usuario** (será parte del enlace del
   repositorio: `https://github.com/SU-USUARIO/paulinum_lab`; conviene algo sobrio, por ejemplo su
   apellido o sus iniciales).
3. Verifique el correo con el código que le envían. Elija el plan **Free** (gratuito).

## Paso 2. Crear el repositorio (la «carpeta» en GitHub)

1. Una vez dentro, pulse el signo **+** arriba a la derecha → **New repository**.
2. **Repository name**: `paulinum_lab`.
3. **Description** (opcional): `Laboratorio de reproducibilidad: verificación convergente de la autoría del corpus paulino canónico (reconstrucción)`.
4. Marque **Public** (cualquier persona con el enlace podrá verlo y descargarlo; nadie podrá modificarlo
   sin su permiso).
5. **No marque** «Add a README file», ni «Add .gitignore», ni «Choose a license»: la carpeta ya los trae.
6. Pulse **Create repository**. Deje abierta esa página: muestra el enlace del repositorio, que tendrá la
   forma `https://github.com/SU-USUARIO/paulinum_lab`.

## Paso 3. Instalar GitHub Desktop

1. Descargue la aplicación en https://desktop.github.com (Windows y Mac) e instálela.
2. Ábrala. Pulse **Sign in to GitHub.com** e inicie sesión con la cuenta del paso 1 (se abre el navegador;
   autorice la aplicación).
3. Cuando pida nombre y correo para las «confirmaciones» (commits), deje los que propone y pulse
   **Finish**.

## Paso 4. Conectar la carpeta paulinum_lab con el repositorio

1. En GitHub Desktop: menú **File → Add local repository…**.
2. Pulse **Choose…** y seleccione la carpeta `paulinum_lab` de su ordenador
   (por ejemplo `C:\Users\ferpe\Desktop\Correccion_Fondo\paulinum_lab`).
3. GitHub Desktop dirá que la carpeta «no parece ser un repositorio Git» y ofrecerá **create a
   repository here instead**. Pulse ese enlace.
4. En la ventana que aparece, deje el nombre `paulinum_lab`, **desmarque** «Initialize this repository
   with a README» (ya existe) y en «Git Ignore» deje **None** (ya hay un `.gitignore`). Pulse **Create
   Repository**.
5. Verá a la izquierda la lista de todos los archivos («Changes»). Abajo a la izquierda, en el cuadro
   **Summary**, escriba: `Reconstrucción del laboratorio paulinum (0.2.0-r)`. Pulse **Commit to main**.
   (Un *commit* es una «fotografía» del estado de la carpeta con una nota.)
6. Ahora pulse el botón **Publish repository** (arriba). En la ventana: nombre `paulinum_lab`,
   **desmarque** «Keep this code private» (para que sea público) y pulse **Publish repository**.
   Si le pregunta a qué cuenta u organización, elija su usuario.

   *Si en el paso 2 ya creó el repositorio vacío en la web, GitHub Desktop puede avisar de que ya existe:
   en ese caso vaya a **Repository → Repository settings… → Remote** y pegue el enlace del paso 2
   (`https://github.com/SU-USUARIO/paulinum_lab.git`); guarde y pulse **Push origin**.*

7. Espere a que termine la subida (barra de progreso). Abra en el navegador
   `https://github.com/SU-USUARIO/paulinum_lab`: verá la carpeta con el README mostrado debajo.

## Paso 5. Comprobar que está todo

En la página del repositorio debe ver, entre otros: `README.md`, `LEEME_PRIMERO.md`, `paulinum/`,
`scripts/`, `config/`, `metadata/`, `results/`, `results_publicados/`, `informes/`, `investigacion_1/`,
`docs/`, `LICENSE`, `LICENSE-DATA`, `CITATION.cff`, `requirements.txt`. No debe ver `data/raw/` ni
`data/cache/` (están excluidos a propósito; `data/local/LEEME_3Cor.md` y `data/provenance.json` sí
aparecen).

## Paso 6. Dar el enlace al director de tesis

Basta enviar `https://github.com/SU-USUARIO/paulinum_lab`. Quien lo reciba puede:
- leerlo en el navegador (empezando por `LEEME_PRIMERO.md` y `README.md`);
- descargarlo entero con el botón verde **Code → Download ZIP**;
- ejecutar las órdenes del README para rehacer cualquier cifra.

## Paso 7. Cuando cambie algo en la carpeta

Cada vez que modifique o añada archivos en `paulinum_lab` (por ejemplo, cuando prepare
`data/local/3Cor.txt` o ejecute una campaña completa y quiera publicar sus resultados):
1. Abra GitHub Desktop: en «Changes» aparecen los archivos modificados.
2. Escriba un resumen (p. ej. `Añadido 3 Corintios preparado` o `Resultados de la campaña 03`) y
   pulse **Commit to main**.
3. Pulse **Push origin** (arriba). El repositorio en la web se actualiza en segundos; el historial de
   versiones queda guardado y cualquier versión anterior sigue siendo consultable.

## Paso 8 (recomendado). Un identificador permanente para citar: Zenodo

Para que el laboratorio se pueda citar en la tesis con un identificador permanente (DOI):
1. Entre en https://zenodo.org y pulse **Log in → Log in with GitHub**; autorice.
2. En Zenodo, menú de la cuenta → **GitHub**. Aparece la lista de sus repositorios; active el interruptor
   de `paulinum_lab`.
3. En GitHub, en la página del repositorio, pulse **Releases → Create a new release**; en «Choose a tag»
   escriba `v0.2.0-r`, pulse «Create new tag», ponga título `paulinum_lab 0.2.0-r (reconstrucción)` y
   pulse **Publish release**.
4. En unos minutos Zenodo archiva esa versión y le asigna un DOI (aparece en su página de Zenodo).
   Añada el DOI al `CITATION.cff` y al README (y confirme el cambio como en el paso 7).

## Problemas frecuentes

- **«Authentication failed»** al publicar: cierre GitHub Desktop, vuelva a abrirlo y repita
  **File → Options → Accounts → Sign in**.
- **Un archivo supera 100 MB**: GitHub lo rechaza. Solo puede ocurrir si copia dentro de la carpeta
  descargas o corpus grandes fuera de `data/raw/` y `data/cache/`; muévalos a esas carpetas (excluidas)
  o bórrelos y repita el commit.
- **Quiere que el repositorio sea privado un tiempo**: en la web, **Settings → General → Danger Zone →
  Change repository visibility → Private**. Podrá invitar a personas concretas en **Settings →
  Collaborators**.
- **Quiere volver a un estado anterior**: en GitHub Desktop, pestaña **History**, botón derecho sobre
  un commit → **Revert changes in commit**.
