import arcpy

def zoom_to_plss_location(feature_class, state_field, township_field, range_field, section_field, target_state, target_township, target_range, target_section):
    # Create a query to select the target PLSS location
    query = f"{state_field} = '{target_state}' AND {township_field} = {target_township} AND {range_field} = {target_range} AND {section_field} = {target_section}"
    print(query)
    # Create a feature layer to perform the selection
    selectFL = "selectedFeatures"
    arcpy.MakeFeatureLayer_management(feature_class, selectFL, query)
    outLoc = arcpy.GetParameterAsText(4)
    outFC = outLoc + r"\temp.shp"
    if not os.path.exists(outLoc):
        os.makedirs(outLoc)
    arcpy.management.CopyFeatures(selectFL, outFC)
    arcpy.analysis.Buffer(selectFL, outFC, ".25 Miles")
    if int(arcpy.GetCount_management(outFC)[0]) == 0:
        arcpy.AddError("This legal description is not in this database.")
        raise arcpy.ExecuteError

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
target_state = arcpy.GetParameterAsText(0)
target_township = arcpy.GetParameterAsText(1)
target_range = arcpy.GetParameterAsText(2)
target_section = arcpy.GetParameterAsText(3)

# Call the function to zoom to the specified PLSS location
zoom_to_plss_location(feature_class, state_field, township_field, range_field, section_field,
                      target_state, target_township, target_range, target_section)
