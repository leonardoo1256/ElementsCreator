import subprocess

# Desarrollado por: Hebert Leonardo Ardila Rivera
# Email: hebert.ardila@ibm.com - hebert_leonardo06@hotmail.com
# 10 de Octubre de 2019

pathProject = input('Ingrese el PATH donde desea crear el proyecto Angular: ')
while(subprocess.call('cd ' + pathProject,shell=True) != 0):
    pathProject = input('Ingrese el PATH donde desea crear el proyecto Angular: ')
nameProject = input('Ingrese el nombre del proyecto: ')
prefix = input('Ingrese el prefijo: ')

installAngularCommand = 'cd '+ pathProject +' && npm install -g @angular/cli'
createProjectCommand = 'cd '+ pathProject +' && ng new '+ nameProject + ' --prefix '+prefix
subprocess.call(installAngularCommand, shell=True)
print("Se instalo la ultima version de Angular")
subprocess.call(createProjectCommand, shell=True)
print('Proyecto ' +prefix+nameProject +' creado con exito')

subprocess.call("cd "+ pathProject+"/"+nameProject +" && ng add @angular/elements",shell=True)
print('Se añadio la libreria Angular Elements')

subprocess.call("cd "+ pathProject+"/"+nameProject + ' && npm install --save classlist.js',shell=True)
subprocess.call("cd "+ pathProject+"/"+nameProject + ' && npm install --save web-animations-js',shell=True)
subprocess.call("cd "+ pathProject+"/"+nameProject + ' && npm install --save document-register-element@1.8.1',shell=True)
print('Se instalaron dependencias para obtener compatibilidad con distintos navegadores')

pathAppModule = pathProject+'/' + nameProject + '/src/app/app.module.ts'
with open(pathAppModule, 'r+') as fd:
    contents = fd.readlines()
    contents.insert(2, "import { Injector } from '@angular/core'; \n")
    contents.insert(3, "import { createCustomElement } from '@angular/elements';")
    fd.seek(0)
    fd.writelines(contents)

with open(pathAppModule, 'r+') as fd:
    contents = fd.readlines()
    fd.seek(0)
    for line in contents:
        if line.find('export class AppModule { }') != -1:
            fd.write("export class AppModule {\n constructor(private injector: Injector) {\n const el = createCustomElement(AppComponent, { injector });\n customElements.define('"+ nameProject+"-elements', el);\n   }\n   ngDoBootstrap() {}\n }")
        else:
            fd.write(line)

with open(pathAppModule, 'r+') as fd:
    contents = fd.readlines()
    fd.seek(0)
    for line in contents:
        if line.find('  bootstrap: [AppComponent]') != -1:
            fd.write('  entryComponents: [AppComponent]\n //  bootstrap: [AppComponent]\n')
        else:
            fd.write(line)

pathConfigJson = pathProject+'/'+ nameProject + '/tsconfig.json'
with open(pathConfigJson, 'r+') as fd:
    contents = fd.readlines()
    fd.seek(0)
    for line in contents:
        if line.find('"target": "es2015",') != -1:
            fd.write('    "target": "es5",\n')
        else:
            fd.write(line)

f = open( pathProject+'/'+ nameProject + '/elements-build.js','a')
f.write("const fs = require('fs-extra');  \nconst concat = require('concat'); \n(async function build() {\n\n    const files = [\n        './dist/"+nameProject+"/runtime.js',\n        './dist/"+nameProject+"/polyfills.js',\n        './dist/"+nameProject+"/scripts.js',\n        './dist/"+nameProject+"/main.js'\n    ];\n    await fs.ensureDir('elements');\n    await concat(files, 'elements/"+nameProject+"-elements.js');\n    await fs.copyFile(\n        './dist/"+nameProject+"/styles.css',\n        'elements/styles.css'\n    );\n})();")
f.close()

subprocess.call("cd "+ pathProject+"/"+nameProject + ' && npm install fs-extra --save-dev',shell=True)
subprocess.call("cd "+ pathProject+"/"+nameProject + ' && npm install concat --save-dev',shell=True)
print('Se instalaron las dependencias necesarias para ejecutar el Script')

pathPackageJson = pathProject+'/'+ nameProject + '/package.json'
with open(pathPackageJson, 'r+') as fd:
    contents = fd.readlines()
    contents.insert(9,'    "build:elements": "ng build --prod --output-hashing none && node elements-build.js",\n')
    fd.seek(0)
    fd.writelines(contents)

subprocess.call("cd "+ pathProject+"/"+nameProject + ' && npm i -D @angular-builders/custom-webpack',shell=True)
print('Se instalo angular-builders')

pathAngularJson = pathProject+"/"+nameProject + '/angular.json'
with open(pathAngularJson, 'r+') as fd:
    contents = fd.readlines()
    contents.insert(13, '            "builder": "@angular-builders/custom-webpack:browser",\n  //')
    contents.insert(18,'            "customWebpackConfig": {\n            "path": "./extra-webpack.config.js",\n            "mergeStrategies": { "externals": "replace" } },\n')
    fd.seek(0)
    fd.writelines(contents)

extraWeb = open(pathProject+'/'+ nameProject + '/extra-webpack.config.js','a')
extraWeb.write("module.exports = {\n    output: {\n      jsonpFunction: '"+nameProject+"-elements',\n      library: '"+nameProject+"elements'\n    }\n};")
extraWeb.close()
print('Modificaciones de archivos realizadas con exito')

subprocess.call("cd "+ pathProject+"/"+nameProject + ' && npm run build:elements',shell=True)
print('Se lanzo el Script de compilacion de manera exitosa')
subprocess.call("cd "+ pathProject+"/"+nameProject + '&& npm -g install static-server', shell=True)
print('Se instalo static-server')

indexElements = open(pathProject+'/'+nameProject+'/elements/index.html','a')
indexElements.write('<!doctype html>\n<html lang="es">\n\n<head>\n    <meta charset="utf-8">\n    <title>Angular Elements</title>\n    <base href="/">\n    <linl rel="stylesheet" type="text/css" href="styles.css">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    </head>\n\n<body>\n    <'+nameProject + '-elements></'+nameProject+'-elements>\n    <script type="text/javascript" src="'+nameProject+'-elements.js"></script>\n</body>\n\n</html> ')
indexElements.close()
print('Se creo el archivo index.html en elements')