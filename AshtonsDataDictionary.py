# -*- coding: utf-8 -*-
# MySQL Workbench module
# <description>
# Written in MySQL Workbench 6.3.10

from wb import *
import grt
from mforms import Utilities, FileChooser
import mforms
import datetime
import os

#ModuleInfo = DefineModule(name="DDReport", author="Ashton Lamont", version="1.0", description="Data Dictionary in HTML format")
#@ModuleInfo.plugin("rsn86.DBDocPy.DataDicthtmlReport", caption="Data Dictionary in HTML format", description="Data Dictionary report in HTML format", input=[wbinputs.currentCatalog()], pluginMenu="Model")
#@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
#ModuleInfo = DefineModule(AshtonDataDictionary)
#@ModuleInfo.export()

filePath=""
newPath=""
docProject=""

def connection():
    pass

def findModels(models,path):
    for m in models:
        findSchemas(m.catalog.schemata,path)
        #print(m)
    pass

def findSchemas(schemata, path):
    for s in schemata:
        newPath=""
        sn = s.name
        print(sn)
        newPath = path + "//%s" % (sn)
        print(newPath)
        if os.path.exists(newPath):
            #maybe delete and recreate here
            print("Folder Exists")
        else:
            os.makedirs(newPath)
        htmlSchemaFiles(s,newPath)
    pass
    

def ashtondatadictionary():
    #print(grt.root.wb.doc)
    global filePath
    filePath = chooseFolder()
    #global filePath
    #filePath = os.path.dirname(fullFilePath)
    global docProject
    docProject = grt.root.wb.doc.info.project

    newPath=""
    newPath=filePath + "//%s" % (docProject)
    print(newPath)

    if os.path.exists(newPath):
        #maybe delete and recreate here
        print("Folder Exists")
    else:    
        os.makedirs(newPath)
    
    global filePath
    indexPath=filePath + "//index.html"
    textStart ="""<html><head><title>Schema Report</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
        }
        iframe {
            height:100%;
            width:100%;
        }
        /* Style the side navigation */
        .sidenav {
            color:white;
            height: 100%;
            width: 350px;
            position: fixed;
            z-index: 1;
            top: 0;
            left: 0;
            background-color: navy;
            overflow-x: hidden;
        }


        /* Side navigation links */
        .sidenav a {
            color: white;
            padding: 5px;
            text-decoration: none;
            display: block;
        }

        /* Change color on hover */
        .sidenav a:hover {
            background-color: #ddd;
            color: black;
        }
        /* Style the content */
        .content {
            margin-left: 350px;
            padding-left: 20px;
        }
        </style>
      </head><body><div class="sidenav"><b>Schema and Table List: schema.table</b><br/>"""
    writeToFile(indexPath,textStart,"w")
    

    findModels(grt.root.wb.doc.physicalModels,newPath)
    #print(filePath)
    textEnd = """</div><div class="content"><iframe id="tableFrame" src="blank.html" ></div></body></html>"""
    writeToFile(indexPath,textEnd,"a")
    pass

def chooseFolder():
    # Put plugin contents here
    path= ""
    filechooser = FileChooser(mforms.OpenDirectory)
    if filechooser.run_modal():
       path = filechooser.get_path()
    print "HTML File: %s" % (path)

    if len(path) >= 1:
        #print(path)
        return path
    pass

def writeToFile(path,text,mode):
    print(path)
    if mode == "a":
        tFile = open(path, "a") # a - append, w - overwrite
    elif mode == "w":
        tFile = open(path, "w")
    print >>tFile, text
    tFile.close()

def htmlSchemaFiles(schema,path):
    # iterate through columns from schema
    sn = schema.name
    text=""
    global docProject
    for table in schema.tables:
      text=""
      text="""<style>
            .header{
                background-color: navy;
                color: white;
                font-weight: bold;
                } 
            .header2{
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                }
            .row{
                background-color: #85C1E9 ;
                color: black;
                font-weight: bold;
                }
        </style>"""
      tn = table.name
      newPath=path + "//%s.html" % (tn)
      link = "<a href=\"#\" onclick=\"javascript:document.getElementById('tableFrame').src='./%s/%s/%s.html'\">%s.%s </a>" % (docProject,sn,tn,sn,tn)
      global filePath
      listPath=filePath + "//index.html"
      writeToFile(listPath,link,"a")
      
      text += "<a id=\"%s.%s\"></a>" % (sn,tn)
      text += "<table style=\"width:100%\">"
      text += "<tr><th colspan=9 class='header'>Table: %s.%s</th></tr>" % (sn,tn)
      text += "<tr class='row'><td>Table Comments</td><td colspan=\"8\">%s</td></tr>" % (table.comment)
      text += """<tr><th colspan="9" class='header'>Columns</th></tr>
        <tr>
        <th class="header2">Name</th>
        <th class="header2">Data Type</th>
        <th class="header2">Nullable</th>
        <th class="header2">PK</th>
        <th class="header2">FK</th>
    	<th class="header2">AI</th>
        <th class="header2">UN</th>
        <th class="header2">Default</th>
        <th class="header2">Comment</th>
        </tr>"""
      for column in table.columns:
        pk = ('No', 'Yes')[bool(table.isPrimaryKeyColumn(column))]
        fk = ('No', 'Yes')[bool(table.isForeignKeyColumn(column))]
        nn = ('No', 'Yes')[bool(column.isNotNull)]
        ai = ('No', 'Yes')[bool(column.autoIncrement)]
        un = 'n/a' #('No', 'Yes')[bool(column)]
        text += "<tr class='row'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (column.name,column.formattedType,nn,pk,fk,ai,un,column.defaultValue,column.comment)
      text += """<tr><th colspan=\"9\"  class='header'>Indexes</th></tr>
        <tr>
        <th class="header2">Name</th>
        <th class="header2">Type</th>
        <th class="header2">Columns</th>
        <th class="header2" colspan="6">Comment</th>
        </tr>"""
      for index in table.indices:
	# index name
    	idn = index.name

    	# index columns
    	ic = ""
        ic = ", ".join(str(c.referencedColumn.name) for c in index.columns)

    	# index type
    	it = index.indexType

    	# index description
    	id = index.comment
        text += "<tr class='row'><td>%s</td><td>%s</td><td>%s</td><td colspan='6'>%s</td></tr>" % (idn,it,ic,id)
        #text += "</table></body></html>"
        #print(text)
      writeToFile(newPath,text,"w")
    #Utilities.show_message("Report generated", "HTML Report format from current model generated", "OK","","")
    return 0

ashtondatadictionary()
