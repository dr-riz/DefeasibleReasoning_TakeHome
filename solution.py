#!/usr/bin/env python3
# CPU-only, standard library only
import csv
import json
import urllib.request
import sys
from typing import Dict, List, Tuple

class LLMReasoner:
    """Uses local Ollama API with <llm_model> model for defeasible reasoning"""
    
    def __init__(self):
        self.api_endpoint = "http://localhost:11434/api/generate"
        self.model = "phi3"  # Make sure to run 'ollama pull <llm_model>' first
        # first_shot classifier = 0.5
        # smollm:135m=0.1
        # smoll:latest=0.2 (1.7b)
        # phi=0.1
        # phi=0.5 (175b)
    def format_prompt(self, facts: str, rules: str, preferences: str, question: str) -> str:
        """Format the input as a natural language prompt for the LLM"""
        return f"""Given these facts:
{facts}

And these rules:
{rules}

With rule preferences (higher priority rules override lower ones):
{preferences}

Please determine if the following is Proved, Disproved, or Unknown:
{question}

Analyze the rules and facts carefully. A conclusion is:
- Proved if a supporting rule applies and is not overridden
- Disproved if a blocking rule applies and is not overridden
- Unknown if no rules apply or there are unresolved conflicts

Answer with exactly one word: Proved, Disproved, or Unknown"""

    def query_llm(self, prompt: str) -> str:
        """Query the local Ollama API"""
        data = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': 0.1,  # Low temperature for more deterministic reasoning
                'num_predict': 10    # Limit response length
            }
        }
        
        try:
            headers = {'Content-Type': 'application/json'}
            request = urllib.request.Request(
                self.api_endpoint,
                data=json.dumps(data).encode(),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(request) as response:
                result = json.loads(response.read().decode())
                
            # Extract just the classification from the response
            text = result['response'].strip().lower()
            
            # Normalize to one of our three valid outputs
            if 'proved' in text:
                return 'Proved'
            elif 'disproved' in text:
                return 'Disproved'
            return 'Unknown'
            
        except Exception as e:
            print(f"Ollama API error: {e}", file=sys.stderr)
            return self.rule_based_reasoning(prompt)
            
    def rule_based_reasoning(self, prompt: str) -> str:
        """Fallback method using simple rule-based reasoning"""
        # Simple heuristics if API fails
        text = prompt.lower()
        if "no attacks" in text and ">" in text:
            return "Proved"
        if "attacks" in text:
            return "Disproved"
        if "older than" in text and "internet device" not in text:
            return "Proved"
        return "Unknown"

def predict_row(facts: str, rules: str, preferences: str, question: str) -> str:
    """Process a single row from the dataset"""
    reasoner = LLMReasoner()
    prompt = reasoner.format_prompt(facts, rules, preferences, question)
    return reasoner.query_llm(prompt)

def eval_csv(path: str) -> float:
    """Evaluate all rows in the CSV file"""
    total, correct = 0, 0
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pred = predict_row(
                row['facts'],
                row['rules'], 
                row['preferences'],
                row['question']
            )
            ok = (pred == row['label'])
            total += 1
            correct += int(ok)
            print(f"id:{row['id']} predicted: {pred} ({'correct' if ok else 'wrong'})")
    
    acc = correct / max(1, total)
    print(f"Overall Accuracy: {acc:.2f}")
    return acc

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'defeasible_tasks.csv'
    eval_csv(path)
