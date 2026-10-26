---
name: Signaler un bug
description: Aider à reproduire un problème
labels: [bug]
body:
  - type: textarea
    id: description
    attributes:
      label: Description du problème
      description: Décrivez ce qui s'est passé et ce que vous attendiez.
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Version de SYNERGIE
      placeholder: V6.1 / EXE téléchargé depuis une Release
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Étapes pour reproduire
      placeholder: 1. Ouvrir SYNERGIE…
    validations:
      required: true
  - type: textarea
    id: error
    attributes:
      label: Message d'erreur (si présent)
      description: Supprimez d'abord les tokens, URL de webhook, identifiants et autres données privées.
