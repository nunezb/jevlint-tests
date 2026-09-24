# Sources, sampling, and traceability

## Sampling summary

The 27 request files were selected from question sets in a measurement program that predates `jevlint`. They were not written against its rule set. The sample pairs query conventions with already recorded outcomes and includes both measured problem cases and measured-clean controls. See `queries/` for the exact requests and `annotations/queries_with_evidence.json` for the evidence summaries used in this report.

The local archive does not contain the source program's full population, raw response logs, or analysis scripts. It also does not record an upstream revision and example ID for every selected public-dataset item. The recorded measurements are therefore traceable to the summaries in `annotations/`, but not all can be recomputed from this repository alone.

## Query groups and upstream sources

| Query files | Source and available pointer | License and traceability |
| --- | --- | --- |
| `q_bayes_claims_*` (5) | Written locally for this study | The annotation marks these questions CC BY 4.0. |
| `q_clean_*` (6) | [MMLU](https://github.com/hendrycks/test), Hendrycks et al., ICLR 2021 | The upstream repository lists MIT ([license](https://github.com/hendrycks/test/blob/master/LICENSE)). This archive does not retain the selected subject/file, item IDs, or upstream revision for each query. |
| `q_folio_*` (4) | [FOLIO](https://github.com/Yale-LILY/FOLIO), Han et al., 2022 | The original dataset repository lists CC BY-SA 4.0 ([license](https://github.com/Yale-LILY/FOLIO/blob/main/LICENSE)). The selected example IDs and exact revision are not recorded here. |
| `q_longstate_*` (3) | Long documents assembled from report text produced in the local workspace | Locally assembled study material; included under the project-authored material notice in `DATA-LICENSE.md`. No public dataset is used. |
| `q_negation_*` (4) | Written locally for this study | The annotation marks these questions CC BY 4.0. |
| `q_origin_overlap_00` (1) | One human answer from [HC3 English](https://huggingface.co/datasets/Hello-SimpleAI/HC3); the matching answer appears at [current train-viewer row 351](https://huggingface.co/datasets/Hello-SimpleAI/HC3/viewer/all/train?p=3) in the `reddit_eli5` subset | The [HC3 project README](https://github.com/Hello-SimpleAI/chatgpt-comparison-detection#dataset-copyright) says the source dataset's stricter terms apply; its source table lists ELI5 under BSD. This archive does not pin an HC3 revision. Preserve the ELI5 attribution and source terms; this repository does not relicense the excerpt. |
| `q_rubric_*` (4) | Locally generated solution rubrics | The annotation marks these items CC BY 4.0. |

The public-dataset references identify the datasets used, not a complete record-level manifest. MMLU and FOLIO row IDs should be added if recovered from the original sampling logs. The HC3 viewer row is a current source pointer, not a pinned revision identifier.

## Citations

- Dan Hendrycks et al. “Measuring Massive Multitask Language Understanding.” ICLR 2021. [Paper](https://arxiv.org/abs/2009.03300) · [dataset/code repository and license](https://github.com/hendrycks/test).
- Simeng Han et al. “FOLIO: Natural Language Reasoning with First-Order Logic.” 2022. [Paper](https://arxiv.org/abs/2209.00840) · [dataset repository and license](https://github.com/Yale-LILY/FOLIO).
- Biyang Guo et al. “How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection.” 2023. [Paper](https://arxiv.org/abs/2301.07597) · [HC3 repository and dataset terms](https://github.com/Hello-SimpleAI/chatgpt-comparison-detection).
