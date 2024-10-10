import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.dao.DataAccessException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ClineDataMappingEventServiceTest {

    @InjectMocks
    private ClineDataMappingEventService clineDataMappingEventService;

    @Mock
    private DataMappingOutboxRepository dataMappingOutboxRepository;

    @Mock
    private DataReceivedToInboxRepository dataMappingInboxRepository;

    @Mock
    private Logger log;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testProcessExpiryDataOutboxEvent_Success() {
        DataReceivedInbox dataReceivedInbox = new DataReceivedInbox();
        dataReceivedInbox.setConstructionlineReferenceNumber("1234");

        // Call the method under test
        clineDataMappingEventService.processExpiryDataOutboxEvent(dataReceivedInbox);

        // Verify that logging was done
        verify(log).info("Processing calculated expiry data event received: {}", dataReceivedInbox);
        verify(log).info("Message has been saved to process expiry data outbox for buyerId: {}", "1234");

        // You can also verify interactions with repositories if needed
        // Example: verify(dataMappingOutboxRepository).save(any());
    }

    @Test
    public void testProcessExpiryDataOutboxEvent_DataAccessException() {
        DataReceivedInbox dataReceivedInbox = new DataReceivedInbox();
        dataReceivedInbox.setConstructionlineReferenceNumber("1234");

        // Simulate DataAccessException
        doThrow(new DataAccessException("Database error") {})
            .when(dataMappingOutboxRepository).save(any());

        // Expect the method to throw a DataAccessException after retries
        assertThrows(DataAccessException.class, () -> {
            clineDataMappingEventService.processExpiryDataOutboxEvent(dataReceivedInbox);
        });

        // Verify logging of the error
        verify(log).error(anyString(), any(DataAccessException.class));
    }
}

