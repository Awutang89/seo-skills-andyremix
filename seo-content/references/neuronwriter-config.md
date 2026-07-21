# NeuronWriter API Config

**IMPORTANT: Credentials have been moved to .env file for security.**

## Setup

1. Copy `.env.example` to `.env`
2. Fill in your NeuronWriter credentials:
   - `NEURONWRITER_API_KEY`
   - `NEURONWRITER_PROJECT_ID`

## Fixed Query Settings

| Setting | Value |
|---|---|
| Engine | google.com |
| Language | English |

**Note:** Language must be the full word `English`, not the code `en`. Using `en` causes the API to return an error.

## Base URL

```
https://app.neuronwriter.com/neuron-api/0.5/writer
```

## Auth Header

```
X-API-KEY: <value from .env file>
```

## Usage in Scripts

All scripts automatically load credentials from `.env`:

```powershell
# Load environment variables
. (Join-Path $PSScriptRoot 'scripts\load-env.ps1')

$headers = @{
    'X-API-KEY' = $env:NEURONWRITER_API_KEY
    'Content-Type' = 'application/json'
}
```
