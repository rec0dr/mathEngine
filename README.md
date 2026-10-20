# Math Engine

Math Engine is an independent Python project built with Pygame to
explore mathematical visualization and interactive graphing. The goal is
to build a flexible graphing engine while learning more about
object-oriented design, mathematical expression modeling, and
interactive application development.

> **Project status:** In active development. Features and internal
> design may change as the project evolves.

## Preview
! [Simple Graph in Math Engine](images/sample1.png)

! [Different Object Types in Math Engine](images/sample2.png)

## Current Features

-   **Graph rendering** for mathematical curves.
    - **Explicit Functions**
    - **Points & Vectors**
    - **Parametric Functions**
-   **Function evaluation and analysis** as part of the graphing system.
-   **Interactive viewport controls**, including panning and zooming.
    - **Customizable Keybinds**
-   **Customizable interface** for interacting with the graphing
    environment.
-   **Object-oriented mathematical expressions**, using custom classes
    and Python operator overloading to construct expressions.

## Technical Overview

Math Engine is written in Python and uses Pygame for its graphical
application.

A central part of the project is representing mathematical expressions
as objects. Custom classes and operator overloading allow mathematical
operations to be composed using familiar Python syntax. The project is
also being developed with an emphasis on separating mathematical
behavior, graph rendering, and user interaction into manageable
components.

This project is an ongoing opportunity to explore software architecture,
computational problem-solving, and the process of refining a program
through iterative development.

## Technology Stack

-   **Language:** Python
-   **Graphics and input:** Pygame
-   **Editor:** Visual Studio Code
-   **Version control:** Git and GitHub

## Running the Project

Running MathEngine is simple; follow the steps below.

1.  Clone or download this repository.
2.  Create a Python virtual environment, or activate the provided venv_win or venv_mac environment 
    if it is compatible with your system.
3.  Install the project's dependencies.
4.  Run main.py to launch the application. 
    The file currently includes a sample implementation demonstrating how to create and display objects. 
    The API and object-creation workflow are still being documented.

## Controls

The application supports viewport navigation, including panning and
zooming, speed changes, and object clears. Keybinds may also be customized via
the main.py file. (Once again, documentation will be added shortly). Until then,
the default controls have been listed below.

**W** - Move in +y direction

**S** - Move in -y direction

**D** - Move in +x direction

**A** - Move in -x direction

**Z** - Zoom out

**X** - Zoom in

**,** - Decrease movement speed

**.** - Increase movement speed

**/** - Reset movement speed

**C** - Clear all objects

## Roadmap

Potential areas for continued development include:

-   Expanding supported mathematical expressions and curve types.
-   Improving graph rendering and mathematical analysis.
-   Refining the user interface and internal architecture.
-   Improving project documentation and setup instructions.
-   Exploring the possibility of a web-based version.

Development progress and significant changes are documented through 
Git commits and project documentation.

## Contributing and Feedback

Math Engine is currently an independent learning project. Feedback,
ideas, and suggestions are welcome as the project develops.

## License

No license has been specified yet. Until a license is added to the
repository, do not assume that the code is licensed for reuse or
redistribution.
