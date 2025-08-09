#!/usr/bin/env python3

# https://chatgpt.com/c/686ad80f-9cb8-800a-8ff7-93bc574e0979
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings
import pyperclip
import os
import subprocess
import shutil

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
TAG_FILE = f"{CURRENT_DIR}/tags_cli.txt"

def load_tags_from_file(filename):
    tags = []
    default_selected = []
    with open(filename, "r") as f:
        for line in f:
            tag = line.strip()
            if not tag:
                continue
            if tag.startswith("*"):
                clean_tag = tag[1:]
                default_selected.append(clean_tag)
                # tags.append(clean_tag)
            else:
                tags.append(tag)
    return tags, default_selected

class TagCompleter(Completer):
    def __init__(self, tags):
        self.tags = tags

    def get_completions(self, document, complete_event):
        word = document.text.lower()
        for tag in self.tags:
            if word in tag.lower():
                yield Completion(tag, start_position=-len(word))

def main():
    if not os.path.exists(TAG_FILE):
        print(f"❌ File not found: {TAG_FILE}")
        return

    all_tags, default_selected = load_tags_from_file(TAG_FILE)
    selected_tags = default_selected.copy()

    # Show default tags
    if default_selected:
        print(f"📌 Default selected tags: {' '.join(default_selected)}\n")
    else:
        print("ℹ️ No default tags selected.")

    # Show all tags
    print(f"📚  Other available tags: {' '.join(all_tags)}")
    print("\n💡 Start typing tags. Press Enter to select, empty input to finish.")
    print("↩️ Press Ctrl+Z to undo last tag selection.")
    print("📝 Press Ctrl+E to edit the tag file.\n")

    # Setup key bindings
    bindings = KeyBindings()

    @bindings.add('c-z')  # Ctrl+Z
    def _(event):
        if selected_tags and len(selected_tags) > len(default_selected):
            removed = selected_tags.pop()
            print(f"↩️ Removed last tag: {removed}")
        else:
            print("⚠️ No tag to undo (or only default tags remain).")


    @bindings.add('c-e')  # Ctrl+E to edit tags file
    def _(event):
        editor = os.environ.get("EDITOR") or shutil.which("nano") or shutil.which("vi")
        if not editor:
            print("❌ No editor found (set $EDITOR or install nano/vi).")
            return

        print(f"📝 Opening tag file with: {editor}")
        event.app.exit()  # exit prompt to avoid UI conflict
        subprocess.run([editor, TAG_FILE])

        # Reload tags
        new_tags, new_defaults = load_tags_from_file(TAG_FILE)
        all_tags.clear()
        all_tags.extend(new_tags)
        default_selected.clear()
        default_selected.extend(new_defaults)
        selected_tags.clear()
        selected_tags.extend(new_defaults)
        print(f"🔄 Tags reloaded. Defaults: {' '.join(default_selected)}")

    while True:
        try:
            text = prompt("> ", completer=TagCompleter(all_tags), key_bindings=bindings)

            if text is None:
                continue  # prompt was interrupted (e.g., Ctrl+E exited it), just re-prompt
            if not text.strip():
                break

            if text in all_tags and text not in selected_tags:
                selected_tags.append(text)
                print(f"✅ Added: {text}")
            elif text in selected_tags:
                print(f"⚠️ Already selected: {text}")
            else:
                print(f"❌ Invalid tag: {text}")
        except KeyboardInterrupt:
            print("\n⛔️ Interrupted. Exiting...")
            return

    result = " ".join(f"#{tag}" for tag in selected_tags)
    pyperclip.copy(result + " ")
    print(f"\n📋 Tags copied to clipboard:\n{result}")

if __name__ == "__main__":
    main()
