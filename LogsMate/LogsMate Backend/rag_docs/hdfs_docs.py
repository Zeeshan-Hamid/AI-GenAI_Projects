from langchain.docstore.document import Document

hdfs_rag_docs = [
    Document(
        page_content="Block blk_38865049064139660 failed verification due to checksum mismatch",
        metadata={
            "description": "Checksum mismatch detected during block transfer",
            "error_type": "ChecksumMismatch",
            "severity": "High",
            "resolution": "Verify network connections and block replication process.",
            "patterns": "failed verification due to checksum mismatch, failed checksum validation for block"
        }
    ),
    Document(
        page_content="Unexpected EOF while reading block blk_38865049064139660",
        metadata={
            "description": "Unexpected EOF detected during block transfer",
            "error_type": "EOFError",
            "severity": "Medium",
            "resolution": "Check for incomplete data transfers and verify network stability.",
            "patterns": "unexpected EOF while reading block"
        }
    ),
    Document(
        page_content="Connection timeout for node /10.251.43.115 while transferring blk_-6670958622368987959",
        metadata={
            "description": "Connection timeout detected during block transfer",
            "error_type": "Timeout",
            "severity": "Medium",
            "resolution": "Investigate network latency and node responsiveness.",
            "patterns": "connection timeout"
        }
    ),
    Document(
        page_content="Block blk_-6670958622368987959 encountered unrecoverable corruption",
        metadata={
            "description": "Unrecoverable corruption detected in block",
            "error_type": "Corruption",
            "severity": "Critical",
            "resolution": "Replace corrupted blocks and ensure replication is consistent.",
            "patterns": "unrecoverable corruption"
        }
    ),
    Document(
        page_content="Exception during block transfer for blk_4568434182693165548: java.io.IOException",
        metadata={
            "description": "Exception detected during block transfer",
            "error_type": "TransferException",
            "severity": "High",
            "resolution": "Verify transfer process and ensure all nodes are functioning correctly.",
            "patterns": "exception during block transfer"
        }
    ),
    Document(
        page_content="Node /10.251.89.155 experiencing repeated data loss events",
        metadata={
            "description": "Node experiencing repeated data loss events",
            "error_type": "DataLoss",
            "severity": "Critical",
            "resolution": "Investigate hardware issues and improve data replication.",
            "patterns": "repeated data loss events"
        }
    )
]