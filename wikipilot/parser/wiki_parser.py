class WikiParser:
    def __init__(self):
        self.state_stack = ["TEXT"]
        self.output = []
        self.buffer = []

    def push_state(self, state):
        self.state_stack.append(state)

    def pop_state(self):
        if len(self.state_stack) > 1:
            self.state_stack.pop()

    def current_state(self):
        return self.state_stack[-1]

    def parse(self, text):
        i = 0
        while i < len(text):
            ch = text[i]
            state = self.current_state()

            # Handle bold+italic
            if text[i:i+5] == "'''''":
                if state == "BOLD_ITALIC":
                    self.flush_buffer()
                    self.pop_state()
                else:
                    self.flush_buffer()
                    self.push_state("BOLD_ITALIC")
                i += 5
                continue

            # Handle bold
            elif text[i:i+3] == "'''":
                if state == "BOLD":
                    self.flush_buffer()
                    self.pop_state()
                else:
                    self.flush_buffer()
                    self.push_state("BOLD")
                i += 3
                continue

            # Handle italics
            elif text[i:i+2] == "''":
                if state == "ITALIC":
                    self.flush_buffer()
                    self.pop_state()
                else:
                    self.flush_buffer()
                    self.push_state("ITALIC")
                i += 2
                continue

            # Handle links
            elif text[i:i+2] == "[[":
                self.flush_buffer()
                self.push_state("LINK")
                i += 2
                continue
            elif text[i:i+2] == "]]" and state == "LINK":
                self.flush_buffer()
                self.pop_state()
                i += 2
                continue

            # Handle templates
            elif text[i:i+2] == "{{":
                self.flush_buffer()
                self.push_state("TEMPLATE")
                i += 2
                continue
            elif text[i:i+2] == "}}" and state == "TEMPLATE":
                self.flush_buffer()
                self.pop_state()
                i += 2
                continue

            # Regular text
            else:
                self.buffer.append(ch)
                i += 1

        self.flush_buffer()
        return self.output

    def flush_buffer(self):
        if not self.buffer:
            return
        state = self.current_state()
        content = "".join(self.buffer)
        self.output.append((state, content))
        self.buffer = []


# Example usage
parser = WikiParser()
text = "This is ''italic'', '''bold''', and '''''bold+italic'''''. Also a [[Link]] and a {{Template}}."
result = parser.parse(text)

for state, content in result:
    print(f"{state}: {content}")
