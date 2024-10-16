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
