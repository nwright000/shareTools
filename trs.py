import arcpy

def zoom_to_plss_location(feature_class, state_field, township_field, range_field, section_field, target_state, target_township, target_range, target_section):
    # Create a query to select the target PLSS location
    query = f"{state_field} = '{target_state}' AND {township_field} = {target_township} AND {range_field} = {target_range} AND {section_field} = {target_section}"
    print(query)
    # Create a feature layer to perform the selection
    selectFL = "selectedFeatures"
    arcpy.MakeFeatureLayer_management(feature_class, selectFL, query)
    result = arcpy.management.GetCount(selectFL)
    if int(result.getOutput(0)) != 0:
        print('shitThere')
    else:
        print('noSuchPlace')
    outFC = r"C:\temp\temp.shp"
    arcpy.analysis.Buffer(selectFL, outFC, ".25 Miles")
    arcpy.management.RecalculateFeatureClassExtent(outFC)

    # Get the extent of the selected features
    extent = arcpy.Describe(outFC).extent
    print(extent)
    arcpy.management.Delete(selectFL)
    arcpy.management.Delete(outFC)

    # Set the current map extent to the extent of the selected features
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    cam = aprx.activeView.camera
    cam.setExtent(extent)

    

    # Refresh the active view
    #arcpy.mp.ArcGISProject("CURRENT").refresh()

# Replace 'C:/path/to/your/geodatabase.gdb/feature_class' with the path to your actual feature class
feature_class = r"https://services.arcgis.com/QVENGdaPbd4LUkLV/arcgis/rest/services/PPJV_PLSS/FeatureServer/11"

# Replace 'STATE_FIELD', 'TOWNSHIP_FIELD', 'RANGE_FIELD', and 'SECTION_FIELD' with the field names
# that store the state, township, range, and section information, respectively, in your feature class
state_field = "State"
township_field = "Township"
range_field = "Range"
section_field = "SECTION"

# Replace 'TargetState', 'TargetTownship', 'TargetRange', and 'TargetSection' with the specific
# state, township, range, and section values you want to zoom to
target_state = "ND"
target_township = 131
target_range = 69
target_section = 24

# Call the function to zoom to the specified PLSS location
zoom_to_plss_location(feature_class, state_field, township_field, range_field, section_field,
                      target_state, target_township, target_range, target_section)
