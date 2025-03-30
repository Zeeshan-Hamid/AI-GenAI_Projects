import time
import logging
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from httpx import ReadTimeout
from fpdf import FPDF
from tqdm import tqdm
import os
import json

global_start_time = time.time()

# Custom memory that stores only AI messages
class AIOnlyMemory(ConversationBufferMemory):
    def save_context(self, inputs, outputs):
        if isinstance(outputs, dict):
            ai_response = (outputs.get("response") or
                           outputs.get("output") or
                           outputs.get("text") or
                           outputs.get("message") or "")
        elif hasattr(outputs, "text"):
            ai_response = outputs.text
        elif isinstance(outputs, str):
            ai_response = outputs
        else:
            ai_response = str(outputs)
        self.chat_memory.add_message(AIMessage(content=ai_response))

# Primary LLM instance for log chunk analysis
# chat_model = ChatMistralAI(
#     mistral_api_key="I3CjMTqdIAYEpQIyheXXsGAROSW5c4Q3",
#     model="mistral-large-latest",
#     temperature=0.3,
#     max_retries=2,
#     max_tokens=50000
# )

chat_model = ChatGoogleGenerativeAI(
    google_api_key="AIzaSyDxXVCbH0L3GQyGlhwbblwUnPwJypFHDLw",
    model="gemini-1.5-flash",
    temperature=0.3,
    max_tokens=50000,
    max_retries=2
)

def run_llm_analysis(index, rag_result):
    memory_instance = AIOnlyMemory(memory_key="history", return_messages=True)
    conversation_instance = ConversationChain(
        llm=chat_model,
        memory=memory_instance,
        verbose=False
    )
    
    print("\n\n Here's the log chunk: ", rag_result['log_chunk'],"\n\n\n")

    context_descriptions = "\n".join([f"- {match['description']}" for match in rag_result['matches']])
    prompt = (
        "INSTRUCTIONS:\n"
        "1. You are analyzing a partial log chunk along with its retrieved context. Your output must be concise, structured as JSON, and suitable for later aggregation.\n"
        "2. First, count the total number of log entries in this chunk. Make sure the count is correct for all the entries. i will not tolerate any faliure in entries count from your side since the system is critical. Each log entry starts with a timestamp like 081109\n"
        "3. Parse each log line to extract a standardized timestamp (ISO8601), log level, component name, and message.\n"
        "4. Identify anomalies by focusing on log entries with severity indicators (e.g., ERROR, CRITICAL or E for ERROR of C for CRITICAL depending upon differnt log files) or specific keywords (e.g., 'SecurityException', 'Screen frozen', 'checksum failure', 'unexpected').\n"
        "5. Deduplicate recurring anomalies: if the same anomaly appears multiple times, report it once with an 'occurrences' count.\n"
        "6. Categorize each anomaly into one of four groups: MEDIUM, HIGH, or CRITICAL. Calculate the count and the percentage (relative to the total anomalies in this chunk) for each category.\n"
        "7. Include a unique 'chunk_id' for traceability.\n"
        "8. Assess the overall system health for this chunk as 'Stable', 'Degraded', or 'Critical'. Make sure your count for anomalies is correct and consider the anomalies count on if they exist in the context I provided.\n"
        "9. Return only a valid JSON output with the following format:\n\n"
        "{\n"
        '  "chunk_id": "<unique identifier>",\n'
        '  "total_log_entries": <integer>,\n'
        '  "anomaly_summary": {\n'
        '      "total_anomalies": <integer>,\n'
        '      "CRITICAL": {"count": <integer>, "percentage": "<percentage>"},\n'
        '      "HIGH": {"count": <integer>, "percentage": "<percentage>"},\n'
        '      "MEDIUM": {"count": <integer>, "percentage": "<percentage>"},\n'     
        "  },\n"
        '  "anomalies": [\n'
        "      {\n"
        '          "timestamp": "ISO8601 format",\n'
        '          "log_level": "E/W/I/D",\n'
        '          "component": "component name",\n'
        '          "anomaly_type": "description",\n'
        '          "occurrences": <integer>,\n'
        '          "details": "concise impact summary"\n'
        "      }\n"
        "      // ... additional anomaly objects\n"
        "  ],\n"
        '  "system_health": "<Stable/Degraded/Critical>"\n'
        "}\n\n"
        " Context on the basis of which you have to consider anomalies inside the log chunk:\n" + context_descriptions + "\n\n"
        "Use the above data as a context for the analysis and the anomalies in the log chunk. Make sure to consider anomalies count on if they exist in the following context.\n"
        "Following is the Log Chunk. Make sure you follow my instructions, use context and provide the correct output:\n" + rag_result['log_chunk'] + "\n\n"
        "Provide the JSON output below:"
    )

    scheduled_time = global_start_time + index * 3
    now = time.time()
    if scheduled_time > now:
        time.sleep(scheduled_time - now)

    try:
        response = conversation_instance.predict(input=prompt)
        logging.info(f"Memory instance: {memory_instance}")
    except ReadTimeout as e:
        logging.error(f"ReadTimeout for chunk {index+1}: {e}. Retrying after delay...")
        time.sleep(8)
        try:
            response = conversation_instance.predict(input=prompt)
            logging.info(f"Memory instance: {memory_instance}")
        except Exception as e2:
            response = f"LLM analysis failed for chunk {index+1} due to error: {e2}"
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error for chunk {index+1}: {error_msg}")
        
        # Check if it's a rate limit error (429)
        if "429" in error_msg and "rate limit" in error_msg.lower():
            logging.info(f"Rate limit exceeded for chunk {index+1}. Switching to alternative API key...")
            
            # Create a new LLM instance with alternative API key
            backup_chat_model = ChatGoogleGenerativeAI(
                google_api_key="AIzaSyCkZDhch_sJgCT4x9yUMJieyjU6gCdLd5w",
                model="gemini-1.5-flash",
                temperature=0.3,
                max_tokens=50000,
                max_retries=2
            )
            
            
            
            # Create new conversation with backup model
            backup_conversation = ConversationChain(
                llm=backup_chat_model,
                memory=memory_instance,
                verbose=False
            )
            
            try:
                logging.info(f"Retrying chunk {index+1} with alternative API key...")
                response = backup_conversation.predict(input=prompt)
                logging.info(f"Successfully processed chunk {index+1} with alternative API key")
            except Exception as backup_error:
                response = f"LLM analysis failed for chunk {index+1} with both API keys. Error: {backup_error}"
        else:
            response = f"LLM analysis failed for chunk {index+1} due to error: {e}"

    return index, response, memory_instance

def generate_final_report(structured_messages, output_pdf="final_report.pdf"):
    time.sleep(5)
    from src.rag import vector_db
    all_rag_data = vector_db._collection.get(include=['documents'])
    rag_data_text = "\n\n".join(all_rag_data['documents'])  # Using double newlines for better separation

    final_chat_model = ChatGoogleGenerativeAI(
                google_api_key="AIzaSyCkZDhch_sJgCT4x9yUMJieyjU6gCdLd5w",
                model="gemini-1.5-pro",
                temperature=0.3,
                max_tokens=50000,
                max_retries=2
            )

    # Convert structured messages to a well-formatted JSON string
    if isinstance(structured_messages, list) and isinstance(structured_messages[0], dict):
        # Already in structured format
        structured_data_json = json.dumps(structured_messages, indent=2)
    else:
        # Legacy format - convert from chat history
        chat_history_text = "\n".join([msg.content for msg in structured_messages])
        structured_data_json = chat_history_text

    final_prompt = (
        "INSTRUCTIONS:\n"
        "You are an expert system analyst. The data below consists of structured outputs from multiple log chunks along with complete RAG context data. The RAG data was used to generate the output for the chunks and the context is provided to you as well so you know on what basis log chunks were analyzed. Each chunk output includes a unique 'chunk_id', the total number of log entries, and an 'anomaly_summary' that provides the total anomalies and counts by severity (MEDIUM, HIGH, CRITICAL). Make sure you combine the count properly. I will not tolerate any ambiguity or faliure in the counts\n"
        "Based on this aggregated information, produce a final, professional, and structured report that includes both a detailed narrative and a structured JSON object.\n\n"
        "Your report should include the following sections:\n"
        "1. The Root cause of anomalies: Provide an overview of all detected anomalies across the analyzed log chunks and the root cause of the anomalies.\n"
        "2. Anomaly Ratios: Report the combined percentage ratios for anomalies categorized as MEDIUM, HIGH, and CRITICAL relative to the total anomalies from all chunks.\n"
        "3. Root Causes: Identify potential root causes for the anomalies, highlighting severe issues where applicable.\n"
        "4. System Health Assessment: Offer an overall assessment of system health based on the aggregated data.\n"
        "5. Actionable Insights: Provide clear recommendations to improve the system.\n\n"
        "Format your final output as a JSON object with the following keys:\n"
        '   "narrative": "A detailed, human-readable report covering all sections above in form of markdown format. Remember that the narrative should be well structured according to report format",\n'
        '   "structured_data": {\n'
        '       "total_log_entries": <integer>(Make sure this combined count of all chunks is correct.),\n'
        '       "total_anomalies": <integer>,\n'
        '       "anomaly_summary": {\n'
        '           "MEDIUM": {"count": <integer>, "percentage": "<percentage relative to total anomalies>"},\n'
        '           "HIGH": {"count": <integer>, "percentage": "<percentage relative to total anomalies>"},\n'
        '           "CRITICAL": {"count": <integer>, "percentage": "<percentage relative to total anomalies>"}\n'
        "       },\n"
        '       "root_causes": [ ... ],\n'
        '       "system_health": "<Stable/Degraded/Critical>",\n'
        '       "actionable_insights": [ ... ]\n'
        "   }\n\n"
        "IMPORTANT: Ensure that your response is ONLY the JSON object with no additional text or markdown formatting. The JSON output must be valid and parseable by standard JSON parsers.\n\n"
        "Aggregated Chunk Data:\n"
        f"{structured_data_json}\n\n"
        "Use following data as context for the report and the anomalies in the combined chunks. You need to conside the following data for analysis and the anomalies in the combined chunks\n"
        f"{rag_data_text}\n\n"
        "Final Report (JSON only):"
    )

    # Get the raw response from the LLM
    raw_response = final_chat_model.predict(text=final_prompt)
    
    # Clean up the response to ensure it's valid JSON
    logging.info(f"Raw LLM response: {raw_response[:500]}...")
    
    # Extract JSON from the response if needed
    cleaned_response = raw_response.strip()
    
    # Handle case where response might be wrapped in code blocks
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response.replace("```json", "", 1)
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
    elif cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.replace("```", "", 1)
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
            
    cleaned_response = cleaned_response.strip()
    
    # Validate JSON and handle errors
    try:
        # Parse and then re-serialize to ensure valid JSON
        parsed_json = json.loads(cleaned_response)
        return json.dumps(parsed_json)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse LLM response as JSON: {str(e)}")
        logging.error(f"Problematic response: {cleaned_response[:1000]}...")
        
        # Create a default JSON object with the raw text as narrative
        fallback_json = {
            "narrative": f"Error parsing LLM response: {raw_response[:5000]}",
            "structured_data": {
                "total_log_entries": 0,
                "total_anomalies": 0,
                "anomaly_summary": {
                    "MEDIUM": {"count": 0, "percentage": "0%"},
                    "HIGH": {"count": 0, "percentage": "0%"},
                    "CRITICAL": {"count": 0, "percentage": "0%"}
                },
                "root_causes": ["Error in analysis generation"],
                "system_health": "Unknown",
                "actionable_insights": ["Retry analysis with different parameters"]
            }
        }
        return json.dumps(fallback_json)
