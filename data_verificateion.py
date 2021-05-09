from collections import namedtuple

tok_next_t = namedtuple('tok_next_t', ['tokens', 'next_state'])

class myFSM:
    def __init__(self):
        self.tok_next = {}

    def add_state(self, name, tokens, next_state):
        if name not in self.tok_next:
            self.tok_next[name] = []
        self.tok_next[name].append(tok_next_t(tokens, next_state))
        
    def run(self, cargo):
        orig_num = cargo
        state = "START"
        err = ""
        while True:
            if(len(cargo) > 0):
                token = cargo[0]
                cargo = cargo[1:]
                found = False
                for tn in self.tok_next[state]:
                    if token in tn.tokens:
                        state = tn.next_state
                        found = True
                        break
                        
                if not found:
                    err = "Got " + token + " in state " + state
                    state = "ERROR"                    
            else:
                if '*' in state:
                    state = "GOOD"
                else:
                    err = "More needed."
                    state = "ERROR"
                    
            if state == "GOOD":
                print(orig_num + " is good.")
                break
            if state == "ERROR":
                print(orig_num + " is bad: " + err)
                break

fsm = myFSM()
fsm.add_state("START", "1234567890", "SECOND_DIGIT_ONWARDS*")
fsm.add_state("START", "-", "AFTER_MINUS")
fsm.add_state("AFTER_MINUS", "1234567890", "SECOND_DIGIT_ONWARDS*")
fsm.add_state("SECOND_DIGIT_ONWARDS*", "1234567890", "SECOND_DIGIT_ONWARDS*")
fsm.add_state("SECOND_DIGIT_ONWARDS*", ".", "AFTER_DOT")
fsm.add_state("AFTER_DOT", "1234567890", "MANTISSA*")
fsm.add_state("MANTISSA*", "1234567890", "MANTISSA*")

fsm.run("3.14")
fsm.run("-7")
fsm.run("-22.0")
fsm.run("--22.0")
fsm.run("-22.a0")
fsm.run("-1.")
fsm.run("-")