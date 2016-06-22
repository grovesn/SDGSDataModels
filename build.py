import glob
import json
import os

__author__ = 'mparker'

BASE_DIR = os.path.dirname(__file__)

schemas = os.path.join(BASE_DIR, "schemas", "IDLs")
ga4gh_schemas = os.path.join(BASE_DIR, "ga4ghSchemas", "IDLs")
openCB_schema = os.path.join(BASE_DIR, "openCBschema", "IDLs")
outfile = os.path.join(BASE_DIR, "protocols", "SDGSProtocols.py")
ga4gh_outfile = os.path.join(BASE_DIR, "protocols", "GA4GHProtocols.py")
avro_tools_jar = os.path.join(BASE_DIR, "resources", "bin", "avro-tools-1.7.7.jar")

for idl in glob.glob(os.path.join(BASE_DIR, "schemas", "IDLs", "*.avdl")):
    print "transforming: " + idl
    base = os.path.basename(idl).replace(".avdl", "")
    os.system("java -jar " + avro_tools_jar + " idl2schemata " + idl + " " +
              os.path.join(BASE_DIR, "schemas", "JSONs", base))

    os.system("java -jar " + avro_tools_jar + " idl " + idl + " " +
              os.path.join(BASE_DIR, "schemas", "AVPRs", base + ".avpr"))


VERSION = json.load(open(os.path.join(BASE_DIR, "schemas", "JSONs", "VersionControl", "VersionControl.avsc")))["fields"][0]["default"]

print "version: " + VERSION


os.system("python " + os.path.join(BASE_DIR, "resources", "CodeGenerationFromGA4GH", "process_schemas.py --outputFile "
                                   + outfile + " --avro-tools-jar " + avro_tools_jar + " --inputSchemasDirectory "
                                   + schemas + " " + VERSION))


os.system("python " + os.path.join(BASE_DIR, "resources", "CodeGenerationFromGA4GH", "process_schemas.py --outputFile "
                                   + ga4gh_outfile + " --avro-tools-jar " + avro_tools_jar + " --inputSchemasDirectory "
                                   + ga4gh_schemas + " " + VERSION))



os.system("avrodoc " + os.path.join(BASE_DIR, "schemas", "AVPRs", "VersionControl.avpr") + " > " + os.path.join(BASE_DIR, "doc", "html_schemas", "VersionControl.html"))
