import sys
import time
from api.service import ask_question
from utils.logger import logger

# Ensure clean UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logger.info("Corrective RAG CLI Interface Initialized")
print("=" * 60)
print("🛡️  CORRECTIVE RAG (CRAG) CLI ASSISTANT")
print("Type your question below, or type 'exit' to quit.")
print("=" * 60)

while True:
    try:
        question = input("\nAsk: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        break

    if not question:
        continue
    if question.lower() == "exit":
        break

    logger.info(f"QUESTION | {question}")
    print("\n⏳ Processing through CRAG agentic graph...")

    result = ask_question(question)

    print("\n" + "=" * 60)
    print("💬 ANSWER:")
    print("=" * 60)
    print(result["answer"])

    print("\n" + "-" * 60)
    print("📊 EXECUTION TELEMETRY & DIAGNOSTICS:")
    print("-" * 60)
    print(f"⏱️  Latency            : {result['latency']:.2f}s")
    print(f"🛡️  Grounded in Facts  : {'YES' if result['grounded'] else 'NO (Corrected/Fallback)'} (Confidence: {int(result['confidence']*100)}%)")
    print(f"🧭 Execution Route     : {result['active_route']}")
    print(f"✍️  Query Rewrites     : {result['rewrite_count']}")
    print(f"🔄 Gen Attempts       : {result['generation_attempts']}")

    if result.get("sources"):
        print(f"📚 Sources Used       : {', '.join(result['sources'])}")

    if result.get("step_history"):
        print(f"⚡ Pathway            : {' -> '.join(result['step_history'])}")

    print("=" * 60)

logger.info("Corrective RAG CLI session ended")