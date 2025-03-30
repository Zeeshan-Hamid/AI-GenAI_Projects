from langchain.docstore.document import Document

android_rag_docs = [
    Document(
        page_content="Aggregated INFO Logs: The Android log file shows numerous routine events including successful acquisition and release of locks, UI visibility changes, surface destructions, and orientation updates. Examples include events like 'acquire lock', 'release lock', 'userActivityNoUpdateLocked', 'setSystemUiVisibility', and 'Destroying surface'. These entries indicate normal system operations.",
        metadata={
            "description": "Aggregated INFO level logs summarizing routine operations such as power management, UI updates, and system resource management on an Android device.",
            "error_type": "Information",
            "severity": "Informational",
            "error_code": "N/A",
            "node_id": "Multiple",
            "log_level": "INFO",
            "resolution": "No action required",
            "patterns": "acquire lock, release lock, userActivityNoUpdateLocked, setSystemUiVisibility, Destroying surface, startAnimation"
        }
    ),
    Document(
        page_content="ERROR: Checksum verification failed for file /system/framework/framework.jar, expected=0xABCD, got=0x1234",
        metadata={
            "description": "Checksum verification failure detected in a critical system file.",
            "error_type": "ChecksumMismatch",
            "severity": "High",
            "error_code": "ECHK_ANDROID1",
            "node_id": "System",
            "log_level": "ERROR",
            "resolution": "Verify file integrity and check for system updates or disk corruption.",
            "patterns": "Checksum verification failed"
        }
    ),
    Document(
        page_content="CRITICAL: Unexpected EOF while reading brightness configuration file /system/etc/brightness.conf",
        metadata={
            "description": "Unexpected EOF detected during the reading of the brightness configuration file.",
            "error_type": "EOFError",
            "severity": "Medium",
            "error_code": "EEOF_ANDROID1",
            "node_id": "DisplayPowerController",
            "log_level": "ERROR",
            "resolution": "Check the integrity of the brightness configuration file and replace if necessary.",
            "patterns": "Unexpected EOF while reading brightness configuration"
        }
    ),
    Document(
        page_content="IOException encountered while destroying surface for com.tencent.qt.qtl/.activity.info.NewsDetailXmlActivity – Resource busy",
        metadata={
            "description": "IOException encountered during surface destruction due to resource contention.",
            "error_type": "IOException",
            "severity": "High",
            "error_code": "EIO_ANDROID1",
            "node_id": "WindowManager",
            "log_level": "ERROR",
            "resolution": "Ensure resource availability and verify that no conflicting operations are occurring.",
            "patterns": "IOException encountered while destroying surface"
        }
    ),
    Document(
        page_content="Data corruption detected in SIM configuration; expected 3 entries, found 2",
        metadata={
            "description": "Data corruption detected in the SIM configuration data.",
            "error_type": "DataCorruption",
            "severity": "Critical",
            "error_code": "ECORR_ANDROID1",
            "node_id": "KeyguardUpdateMonitor",
            "log_level": "ERROR",
            "resolution": "Examine SIM configuration data and restore from backup if necessary.",
            "patterns": "Data corruption detected in SIM configuration"
        }
    ),
    Document(
        page_content="ERROR: Connection timeout while fetching location data from network provider",
        metadata={
            "description": "Connection timeout encountered while attempting to fetch location data.",
            "error_type": "Timeout",
            "severity": "Medium",
            "error_code": "ETIME_ANDROID1",
            "node_id": "PhoneInterfaceManager",
            "log_level": "ERROR",
            "resolution": "Verify network connectivity and check the status of the location service provider.",
            "patterns": "Connection timeout while fetching location data"
        }
    ),
    Document(
        page_content="IOException: Failed to cancel notification for com.tencent.mobileqq – stream closed",
        metadata={
            "description": "IOException occurred during notification cancellation due to a closed stream.",
            "error_type": "NotificationError",
            "severity": "High",
            "error_code": "EIO_ANDROID2",
            "node_id": "NotificationManager",
            "log_level": "ERROR",
            "resolution": "Investigate the notification service and underlying stream issues.",
            "patterns": "Failed to cancel notification"
        }
    ),
    Document(
        page_content="java.lang.ClassCastException: android.os.BinderProxy cannot be cast to com.android.server.am.ActivityRecord$Token",
        metadata={
            "description": "A ClassCastException due to an object type mismatch in the activity manager.",
            "error_type": "ClassCastException",
            "severity": "High",
            "error_code": "ECAST_ANDROID1",
            "node_id": "ActivityManager",
            "log_level": "ERROR",
            "resolution": "Investigate the code or system service for potential type mismatches.",
            "patterns": "cannot be cast to com.android.server.am.ActivityRecord$Token"
        }
    ),
    Document(
        page_content="ANR: Application Not Responding in com.tencent.mm after 5000ms",
        metadata={
            "description": "ANR (Application Not Responding) event detected in com.tencent.mm.",
            "error_type": "ANR",
            "severity": "Critical",
            "error_code": "EANR_ANDROID1",
            "node_id": "ActivityManager",
            "log_level": "ERROR",
            "resolution": "Investigate application performance issues and optimize UI thread responsiveness.",
            "patterns": "ANR: Application Not Responding"
        }
    ),
    Document(
        page_content="SecurityException: Permission denied accessing sensitive data",
        metadata={
            "description": "SecurityException encountered due to an unauthorized attempt to access sensitive data.",
            "error_type": "SecurityException",
            "severity": "High",
            "error_code": "ESEC_ANDROID1",
            "node_id": "System",
            "log_level": "ERROR",
            "resolution": "Review and adjust permission settings as required.",
            "patterns": "Permission denied accessing sensitive data"
        }
    ),
    Document(
        page_content="Native crash detected in libnative.so at offset 0x4F12",
        metadata={
            "description": "A native crash was detected in the system library libnative.so.",
            "error_type": "NativeCrash",
            "severity": "Critical",
            "error_code": "ENATIVE_ANDROID1",
            "node_id": "System",
            "log_level": "ERROR",
            "resolution": "Analyze the native crash dump and inspect memory integrity and library integrity.",
            "patterns": "Native crash detected in libnative.so"
        }
    )
]



