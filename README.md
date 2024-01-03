# GISProject

How to create a Configuration file to update the web map layers popup information..?

step 0: open the config.xml file and update the below information
step 1:  Inside the config section add the Arcgis online portal url and credentials (username & password)
step 2:  Inside the maps section add the web maps that need to be updated and set the enable flag to true, those web maps layers popup will be updated
step 3:  Inside the webMap section add the required layer configuration
Step 4:  update the filed name and aliyas name for each layer and the order of the fields in the layer section as per the config file.
step 5:  similarly add all layers in the same format as shown in the config file
Step 6:  Repeat step 2 - step 5 to add more webmaps as shown in the config file.

application logic.

1) our tool will read the above config.xml file from the specified location mentioned in the configuration file or will fix the location path in the tool then the user must copy the config file in the fixed location.
2) The tool will connect the ArcGIS online portal using the credentials mentioned in the config file, or if you are connected to ArcGIS pro then no need to mention credentials.
3) The tool will access the mentioned web map item IDs from the configuration and update the popup as per the configuration.
