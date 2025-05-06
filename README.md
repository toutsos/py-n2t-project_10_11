
# Nand2Tetris Projects 10 & 11: Jack Compiler

This repository contains an implementation of the Jack Compiler for Nand2Tetris Projects 10 and 11. The compiler translates high-level Jack language programs into VM code, making it possible to run Jack programs on the Hack platform.

## Project 10: Syntax Analyzer

- Implements a **Tokenizer** that breaks Jack code into meaningful tokens (keywords, symbols, identifiers, constants).
- Implements a **Parser** that constructs a hierarchical representation of the Jack program, outputting an XML parse tree.
- Outputs two XML files:
  - `T.xml`: Tokenized version.
  - `P.xml`: Parsed hierarchical tree.

## Project 11: Code Generator

- Completes the compiler by generating **VM code** from Jack source code.
- Handles:
  - Class and subroutine declarations
  - Variable management (local, field, static, argument)
  - Control flow (if, while, return)
  - Expressions and statements
  - Function calls and object construction

- Supports compiling both single `.jack` files and entire directories.

## Usage

Clone the repository:

```bash
git clone 
cd in the project
```

Run the compiler:

For a single `.jack` file:

```bash
python JackCompiler.py path/to/File.jack
```

For a directory of `.jack` files:

```bash
python JackCompiler.py path/to/Directory/
```

Example:

```bash
python JackCompiler.py Square/
```

## Repository Structure

```
├── JackCompiler.py            # Main entry point
├── tokenizer.py               # Tokenizer implementation
├── compilation_engine.py      # Parser and code generator
├── symbol_table.py            # Manages symbol tables
├── vm_writer.py               # Handles VM code output
└── README.md
```

## How It Works

1. **Tokenizer:**
   - Reads the Jack file and converts it into a stream of tokens.

2. **Parser (CompilationEngine):**
   - Parses the token stream into a parse tree.
   - Outputs XML files for debugging in Project 10.

3. **Code Generator:**
   - Walks the parse tree and produces VM commands.
   - Handles symbol resolution and manages scope through a symbol table.

4. **VM Writer:**
   - Writes VM commands to output files.

## Example

Jack Code (`Main.jack`):

```jack
class Main {
    function void main() {
        do Output.printString("Hello, world");
        return;
    }
}
```

Generated VM Code (`Main.vm`):

```
push constant 0
call Output.printString 1
pop temp 0
push constant 0
return
```
