# Qualitative Coding Agent

This repository contains a qualitative coding agent project that utilizes various LangChain and LangGraph components for processing and analyzing qualitative data.

## Project Structure

```
.
├── README.md
├── requirements.txt
└── storage/
    └── (data folders will be stored here)
```

## Setup

1. Create and activate the conda environment:
```bash
conda create -n coding_agent python=3.12 -y
conda activate coding_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Place your data folders containing PDFs in the `storage` directory. Each folder should contain related PDFs for processing. 