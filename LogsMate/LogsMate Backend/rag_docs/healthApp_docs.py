from langchain.docstore.document import Document

healthapp_rag_docs = [
    Document(
        page_content="Aggregated INFO Logs: The HealthApp log shows routine activities including step count updates, calorie calculations, altitude computations, and screen status changes. These entries indicate normal operation of health tracking functions.",
        metadata={
            "description": "Aggregated INFO level logs summarizing routine operations in HealthApp.",
            "error_type": "Information",
            "severity": "Informational",
            "error_code": "N/A",
            "device_id": "Multiple",
            "log_level": "INFO",
            "resolution": "No action required",
            "patterns": "onStandStepChanged, onExtend, getTodayTotalDetailSteps, setTodayTotalDetailSteps, calculateCaloriesWithCache, calculateAltitudeWithCache, REPORT"
        }
    ),
    Document(
        page_content="DATA CORRUPTION: Step count reported as -100, which is invalid.",
        metadata={
            "description": "Data corruption anomaly: invalid negative step count.",
            "error_type": "DataCorruption",
            "severity": "Critical",
            "error_code": "EDATA_CORRUPTION",
            "device_id": "10001234",
            "log_level": "ERROR",
            "resolution": "Investigate sensor readings and data processing pipeline.",
            "patterns": "DATA CORRUPTION, -100"
        }
    ),
    Document(
        page_content="SENSOR FAILURE: Missing heart rate data for the last 5 minutes.",
        metadata={
            "description": "Sensor failure anomaly: missing heart rate data.",
            "error_type": "SensorFailure",
            "severity": "High",
            "error_code": "ESENSOR_FAILURE",
            "device_id": "10004567",
            "log_level": "ERROR",
            "resolution": "Check sensor connectivity and calibration.",
            "patterns": "SENSOR FAILURE, Missing heart rate"
        }
    ),
    Document(
        page_content="NETWORK ERROR: Failed to upload step data to the server.",
        metadata={
            "description": "Network error encountered during data sync.",
            "error_type": "NetworkError",
            "severity": "Medium",
            "error_code": "ENETWORK_ERROR",
            "device_id": "10007890",
            "log_level": "ERROR",
            "resolution": "Check network connectivity and server status.",
            "patterns": "NETWORK ERROR, Failed to upload"
        }
    ),
    Document(
        page_content="PERMISSION DENIED: Unable to access calorie data.",
        metadata={
            "description": "Permission issue: calorie data access denied.",
            "error_type": "PermissionDenied",
            "severity": "High",
            "error_code": "EPERMISSION_DENIED",
            "device_id": "10001234",
            "log_level": "ERROR",
            "resolution": "Review and update permissions for accessing health metrics.",
            "patterns": "PERMISSION DENIED, calorie data"
        }
    ),
    Document(
        page_content="BATTERY ISSUE: Device shutting down due to low power.",
        metadata={
            "description": "Battery issue causing device shutdown.",
            "error_type": "BatteryIssue",
            "severity": "High",
            "error_code": "EBATTERY_ISSUE",
            "device_id": "10005678",
            "log_level": "ERROR",
            "resolution": "Charge the device and investigate battery performance.",
            "patterns": "BATTERY ISSUE, low power"
        }
    ),
    Document(
        page_content="CRASH DETECTED: Unhandled exception in StepDataManager.",
        metadata={
            "description": "Application crash detected due to unhandled exception in StepDataManager.",
            "error_type": "Crash",
            "severity": "Critical",
            "error_code": "ECRASH_DETECTED",
            "device_id": "10009999",
            "log_level": "ERROR",
            "resolution": "Investigate crash logs and update exception handling.",
            "patterns": "CRASH DETECTED, Unhandled exception"
        }
    )
]

