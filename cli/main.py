import uuid
from pathlib import Path
from core.fs_utils import get_desktop_path
from engine.engine import apply_rules, dry_run
from persistence.sqlite import FileHistoryDB


DESKTOP = get_desktop_path()


def manual_mode():
    """Manual organize with dry-run and confirmation"""
    batch_id = uuid.uuid4().hex
    rules_path = Path(__file__).parent.parent / "rules.yaml"
    
    print("\n🔍 DRY RUN - Scanning files...")
    results = dry_run(DESKTOP, rules_path)
    
    if results:
        print("\nProposed changes:")
        for result in results:
            print(f"  {result}")
        print('-------------------------------------')
        confirm = input('Confirm changes? (y/n): ').strip().lower() in ("y", "yes")
        
        if confirm:
            print("\n📦 Applying changes...")
            results = apply_rules(source_directory=DESKTOP, rules_yaml_path=rules_path, batch_id=batch_id)
            print(f"\n✅ Moved {len(results)} files (batch_id: {batch_id})")
        else:
            print("\n❌ Cancelled")
    else:
        print('\n✅ No files to organize')


def watch_mode():
    """Start watch mode for automatic organization"""
    from cli import watch_mode as wm
    print("\n👁️  Starting watch mode...")
    print("Press Ctrl+C to stop\n")
    wm.main()


def undo_mode():
    """Undo the last batch operation"""
    db = FileHistoryDB()
    
    print("\n⏪ Undoing last batch...")
    result = db.undo_batch()
    
    if "message" in result:
        print(f"\n⚠️  {result['message']}")
    else:
        batch_id = result.get('batch_id', 'unknown')
        reverted = result.get('reverted', [])
        failed = result.get('failed', [])
        
        print(f"\nBatch {batch_id}:")
        print(f"✅ Reverted: {len(reverted)} files")
        
        if failed:
            print(f"❌ Failed: {len(failed)} files")
            for src, dst, reason in failed:
                print(f"  - {dst} → {reason}")
    
    db.close()


def show_menu():
    """Display interactive menu"""
    print("\n" + "="*50)
    print("         SORTED - File Auto-Organizer")
    print("="*50)
    print("\nWhat would you like to do?")
    print("  1. Manual organize (dry-run + confirm)")
    print("  2. Watch mode (automatic monitoring)")
    print("  3. Undo last batch")
    print("  4. Exit")
    print("-"*50)


if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            manual_mode()
        elif choice == "2":
            try:
                watch_mode()
            except KeyboardInterrupt:
                print("\n\n👋 Watch mode stopped")
        elif choice == "3":
            undo_mode()
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-4.")

