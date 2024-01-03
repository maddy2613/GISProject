# GISProject

How to create Configuration file to update the web map layers popup inforamtion..?

step1: open config.xml file and update the below information
step1:  Inside the config section add the arcgis online portal url and credentials (username & password)
step2:  Inside the maps section add the web maps whcih needs to be updated and set the enable flag to true, those web maps layers popup will be updated
step3:  Inside the webMap section add the required layer configuration
step4:  update the filed name and aliyas name for each layer and order of the fields in the layer section as per the config file.
step5:  similarly add the all layers in the same format as shown in the config file
step6:  repeat step2 - step5 to add more webmaps as shown in the config file.

application logic.

1) our tool will read the above config.xml file from specified location which mentioned in the configuration file or will fix the location path in the tool then user must copy the config file in the fixed location.
2) tool will connect the arcgis online portal using the credentials whcih mentioned in the config file, or if you connected to ArcGIS pro then no need to mention credentials.
3) tool will access the metioned web map item ids from configuration and update the popup as per the configuration.
