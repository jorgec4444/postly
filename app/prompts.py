# Copyright © 2025 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

"""Prompts used to instruct the language model for tweet improvements.

Each prompt expects a single format argument: {text}.
"""

IMPROVEMENT_PROMPTS: dict[str, str] = {
    "professional": (
        "Eres un experto en contenido profesional para LinkedIn y Twitter/X.\n"
        "Mejora el siguiente tweet para que sea más profesional, claro y valioso.\n"
        "Mantén el mensaje original pero hazlo más impactante.\n"
        "Usa un tono profesional pero accesible.\n"
        "Máximo 280 caracteres.\n\n"
        "Tweet original: {text}\n\n"
        "Devuelve SOLO el tweet mejorado, sin comillas ni explicaciones."
    ),
    "casual": (
        "Eres un experto en contenido casual y cercano para redes sociales.\n"
        "Reescribe el siguiente tweet de manera más conversacional y friendly.\n"
        "Añade emojis apropiados (máximo 2-3).\n"
        "Hazlo más personal y relatable.\n"
        "Máximo 280 caracteres.\n\n"
        "Tweet original: {text}\n\n"
        "Devuelve SOLO el tweet mejorado, sin comillas ni explicaciones."
    ),
    "viral": (
        "Eres un experto en contenido viral para Twitter/X.\n"
        "Transforma el siguiente tweet para maximizar engagement.\n"
        "Usa un hook potente al inicio.\n"
        "Añade estructura con saltos de línea si ayuda.\n"
        "Puede incluir 1-2 emojis estratégicos.\n"
        "Máximo 280 caracteres.\n\n"
        "Tweet original: {text}\n\n"
        "Devuelve SOLO el tweet mejorado, sin comillas ni explicaciones."
    ),
}

VALID_STYLES = frozenset(IMPROVEMENT_PROMPTS.keys())
DEFAULT_STYLE = "professional"
