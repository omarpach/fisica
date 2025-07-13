---
title: "Restricciones"
author: Omar Pacheco
date: July 12, 2025
output: pdf_document
---

# Variables

| $a$ | $\phi$ | $\theta$ |
|-----|--------|----------|
| $\dot{a}$ | $\dot{\phi}$ | $\dot{\theta}$ |
| $\ddot{a}$ | $\ddot{\phi}$ | $\ddot{\theta}$ |
| $V_0$ | $\nu$ | $m^3$ |

# Sistema de ecuaciones de movimiento

- Es un sistema de 3 ecuaciones no lineales, acopladas, diferenciales, ordinarias de segundo orden
```math
\newcommand{\thetadot}{\dot{\theta}}
\newcommand{\thetaddot}{\ddot{\theta}}
\newcommand{\adot}{\dot{a}}
\newcommand{\addot}{\ddot{a}}
\newcommand{\phidot}{\dot{\phi}}
\newcommand{\phiddot}{\ddot{\phi}}

\left\{
    \begin{aligned}
        \addot &= \kappa^2 a \left[ V_0 \left(1 - \frac{\phi^2}{\nu^2} \right)^2 + m^3 \theta \right] - \frac{2 \adot^2}{a} - \frac{2 c^2 K}{a} \\
        \thetaddot &= \frac{2 c^2 \phi}{\nu^2} V_0 \left(1 - \frac{\phi^2}{\nu^2} \right) - \frac{3 \adot \phidot}{a} \\
        \phiddot &= \frac{c^2}{2} m^3 - \frac{3 \adot \thetadot}{a}
    \end{aligned}
\right.
```

Donde $\kappa, c, \text{ y } K$ son constantes, las cuales tendran los valores de $\kappa = 1$, $c = 1$, y $K = 0$, lo cual reduce nuestro sistema de ecuaciones a 

```math
\left\{
    \begin{aligned}
        \addot &= a \left[ V_0 \left(1 - \frac{\phi^2}{\nu^2} \right)^2 + m^3 \theta \right] - \frac{2 \adot^2}{a} \\
        \thetaddot &= \frac{2 \phi}{\nu^2} V_0 \left(1 - \frac{\phi^2}{\nu^2} \right) - \frac{3 \adot \phidot}{a} \\
        \phiddot &= \frac{m^3}{2} - \frac{3 \adot \thetadot}{a}
    \end{aligned}
\right.
```

# Restricciones

Necesitamos encontrar las condiciones iniciales, tales que al resolver el sistema numericamente, se preserven las siguientes condiciones

```math
\begin{align*}
    a,\ \adot,\ \phi,\ \phidot,\ \theta,\ \thetadot,\ \nu,\ V_0,\ m^3 &> 0 \\[0.5em]

    \addot &> 0 \\[0.5em]

    |\eta_{v}(\phi)| = \left| \frac{-4 \left(1 - 3\phi^2 \right) \left(\frac{1}{\nu^2}\right)}{\left(1 - \frac{\phi^2}{\nu^2}\right)^2} \right| &< 0.1 \\[0.5em]

    \epsilon_{v}(\phi) = 8 \left(\frac{\phi}{\nu^2 - \phi^2}\right)^2 &< 0.1 \\[0.5em]

    \left| \ln\left(\frac{a_0}{a_f}\right) - 60 \right| &< 10 \\[0.5em]

    \left| \left( \frac{\adot}{a} \right)^2 - \frac{1}{3} V_0 \left( 1 - \frac{\phi^2}{\nu^2} \right)^2 \right| &< 5 \\[0.5em]

    \left| \phidot + \frac{4}{3} V_0 \left( 1 - \frac{\phi^2}{\nu^2} \right)^2 \left( \frac{\phi a}{\nu^2 \adot} \right) \right| &< 5 \\[0.5em]
\end{align*}
 ```