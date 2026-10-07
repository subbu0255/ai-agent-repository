from agent import run_agent

if __name__ == "__main__":
    print("=" * 72)
    print("MAC REAL DEVICE IT SUPPORT AGENT - POC")
    print("=" * 72)
    print("This version reads REAL metrics from this Mac.")
    print()
    print("Try:")
    print("  My Mac is slow. Diagnose it and create a ticket if necessary.")
    print()
    print("Type 'exit' to quit.\n")

    while True:
        request = input("Employee > ").strip()

        if request.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not request:
            continue

        print("\nAgent is working...\n")

        try:
            answer = run_agent(request)
            print("\nAgent >")
            print(answer)
        except Exception as exc:
            print(f"\nERROR: {exc}")

        print()
