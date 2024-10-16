import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RequiredArgsConstructor
public class JsonMapper {
    
    private final ObjectMapper objectMapper;
    
    public Map<String, Map<String, Object>> mapFields(JsonNode sourceJson, List<Mapping> mappings) {
        Map<String, Map<String, Object>> result = new HashMap<>();

        for (Mapping mapping : mappings) {
            // Get the value from the source JSON using the externalId (dotted path)
            String externalId = mapping.getExternalId();
            JsonNode valueNode = getValueFromJsonByPath(sourceJson, externalId);
            
            if (valueNode != null && !valueNode.isMissingNode()) {
                // Prepare the result with sectionCode and fieldName
                result.computeIfAbsent(mapping.getSectionCode(), k -> new HashMap<>())
                        .put(mapping.getFieldName(), valueNode.asText());
            }
        }
        
        return result;
    }
    
    private JsonNode getValueFromJsonByPath(JsonNode jsonNode, String path) {
        String[] pathParts = path.split("\\.");
        JsonNode currentNode = jsonNode;

        for (String part : pathParts) {
            currentNode = currentNode.path(part);
            if (currentNode.isMissingNode()) {
                break;
            }
        }
        return currentNode;
    }
}



...........................................................

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;

import java.io.IOException;
import java.util.Map;

@RequiredArgsConstructor
public class MappingService {

    private final ObjectMapper objectMapper;
    private final JsonMapper jsonMapper;

    public String processMapping(String sourceJsonString, String mappingJsonString) throws IOException {
        // Parse the source and mappings JSON
        JsonNode sourceJson = objectMapper.readTree(sourceJsonString);
        MappingConfig mappingConfig = objectMapper.readValue(mappingJsonString, MappingConfig.class);

        // Map fields based on the mappings
        Map<String, Map<String, Object>> result = jsonMapper.mapFields(sourceJson, mappingConfig.getMAPPINGS());

        // Convert the result back to JSON
        return objectMapper.writeValueAsString(result);
    }
}
............................................................................



import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RequiredArgsConstructor
public class JsonMapper {
    
    private final ObjectMapper objectMapper;
    
    /**
     * Maps fields from the sourceJson based on the provided list of mappings.
     * 
     * @param sourceJson - The source JSON from which data needs to be mapped.
     * @param mappings - List of mappings that define how to extract and map the data.
     * @return A map where keys are section codes and values are maps of field names and their corresponding values.
     */
    public Map<String, Map<String, Object>> mapFields(JsonNode sourceJson, List<Mapping> mappings) {
        // The result will be a Map where sectionCode is the key and another map of fieldName to value is the value.
        Map<String, Map<String, Object>> result = new HashMap<>();

        // Loop through each mapping
        for (Mapping mapping : mappings) {
            // Get the externalId path from the mapping (e.g., "MainDetails.RegistrationNumber")
            String externalId = mapping.getExternalId();
            
            // Use the helper function to retrieve the value from the source JSON based on the externalId path
            JsonNode valueNode = getValueFromJsonByPath(sourceJson, externalId);
            
            if (valueNode != null && !valueNode.isMissingNode()) {
                // If the value is found, add it to the result map under the appropriate sectionCode and fieldName
                result.computeIfAbsent(mapping.getSectionCode(), k -> new HashMap<>())
                      .put(mapping.getFieldName(), valueNode.asText()); // Store the value in the result map
            }
        }
        
        return result; // Return the final mapped output
    }
    
    /**
     * Helper method to retrieve a value from the source JSON using a dot-separated path.
     * 
     * @param jsonNode - The root JSON node (source).
     * @param path - The dot-separated path to the target field (e.g., "MainDetails.RegistrationNumber").
     * @return The JsonNode representing the value at the specified path, or null if not found.
     */
    private JsonNode getValueFromJsonByPath(JsonNode jsonNode, String path) {
        String[] pathParts = path.split("\\."); // Split the path into individual keys by the dot character
        JsonNode currentNode = jsonNode;

        // Iterate through each part of the path
        for (String part : pathParts) {
            currentNode = currentNode.path(part); // Traverse down the JSON structure
            if (currentNode.isMissingNode()) {
                break; // If the node is missing at any point, break the loop
            }
        }
        return currentNode; // Return the found node or missing node
    }
}

