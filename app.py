{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "bfad0165-851b-4004-9146-f55330a146b6",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import plotly.express as px"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "22d046a4-5bf7-4c1f-a4bd-57a549f318ba",
   "metadata": {},
   "outputs": [],
   "source": [
    "diagnostica = pd.read_csv(\"df_diagnostico.csv\")\n",
    "somativa = pd.read_csv(\"df_somativa.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "35e7c189-43b5-4471-a0eb-1e3fcbdf50b7",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.plotly.v1+json": {
       "config": {
        "plotlyServerURL": "https://plot.ly"
       },
       "data": [
        {
         "hovertemplate": "HABILIDADE - FAIXA=Baixo<br>HABILIDADE - DESCRIÇÃO=%{x}<br>HABILIDADE - ACERTO %=%{text}<extra></extra>",
         "legendgroup": "Baixo",
         "marker": {
          "color": "#000001",
          "pattern": {
           "shape": ""
          }
         },
         "name": "Baixo",
         "orientation": "v",
         "showlegend": true,
         "text": {
          "bdata": "AAAAAAAAAAAAAAAAAAAgQAAAAAAAADdA",
          "dtype": "f8"
         },
         "textposition": "outside",
         "texttemplate": "%{text:.1f}%",
         "type": "bar",
         "x": [
          "Utilizar perímetro de figuras bidimensionais na resolução de problema.",
          "Identificar as marcas linguísticas que evidenciam o locutor e o interlocutor de um texto.",
          "Identificar composições ou decomposições de números naturais."
         ],
         "xaxis": "x",
         "y": {
          "bdata": "AAgX",
          "dtype": "i1"
         },
         "yaxis": "y"
        },
        {
         "hovertemplate": "HABILIDADE - FAIXA=Médio Baixo<br>HABILIDADE - DESCRIÇÃO=%{x}<br>HABILIDADE - ACERTO %=%{text}<extra></extra>",
         "legendgroup": "Médio Baixo",
         "marker": {
          "color": "#000002",
          "pattern": {
           "shape": ""
          }
         },
         "name": "Médio Baixo",
         "orientation": "v",
         "showlegend": True,
         "text": {
          "bdata": "AAAAAACARkAAAAAAAABJQAAAAAAAAElAAAAAAAAASUAAAAAAAIBNQA==",
          "dtype": "f8"
         },
         "textposition": "outside",
         "texttemplate": "%{text:.1f}%",
         "type": "bar",
         "x": [
          "Utilizar números naturais, envolvendo diferentes significados da multiplicação ou da divisão, na resolução de problemas.",
          "Identificar a finalidade de textos de diferentes gêneros.",
          "Corresponder o horário de início e de término com o intervalo de duração de um evento ou acontecimento.",
          "Corresponder figuras tridimensionais às suas planificações.",
          "Determinar o número desconhecido que torna verdadeira uma igualdade matemática envolvendo representação simbólica."
         ],
         "xaxis": "x",
         "y": {
          "bdata": "LTIyMjs=",
          "dtype": "i1"
         },
         "yaxis": "y"
        }
       ],
       "layout": {
        "barmode": "relative",
        "legend": {
         "title": {
          "text": "HABILIDADE - FAIXA"
         },
         "tracegroupgap": 0
        },
        "template": {
         "data": {
          "candlestick": [
           {
            "decreasing": {
             "line": {
              "color": "#000033"
             }
            },
            "increasing": {
             "line": {
              "color": "#000032"
             }
            },
            "type": "candlestick"
           }
          ],
          "contour": [
           {
            "colorscale": [
             [
              0,
              "#000011"
             ],
             [
              0.1111111111111111,
              "#000012"
             ],
             [
              0.2222222222222222,
              "#000013"
             ],
             [
              0.3333333333333333,
              "#000014"
             ],
             [
              0.4444444444444444,
              "#000015"
             ],
             [
              0.5555555555555556,
              "#000016"
             ],
             [
              0.6666666666666666,
              "#000017"
             ],
             [
              0.7777777777777778,
              "#000018"
             ],
             [
              0.8888888888888888,
              "#000019"
             ],
             [
              1,
              "#000020"
             ]
            ],
            "type": "contour"
           }
          ],
          "contourcarpet": [
           {
            "colorscale": [
             [
              0,
              "#000011"
             ],
             [
              0.1111111111111111,
              "#000012"
             ],
             [
              0.2222222222222222,
              "#000013"
             ],
             [
              0.3333333333333333,
              "#000014"
             ],
             [
              0.4444444444444444,
              "#000015"
             ],
             [
              0.5555555555555556,
              "#000016"
             ],
             [
              0.6666666666666666,
              "#000017"
             ],
             [
              0.7777777777777778,
              "#000018"
             ],
             [
              0.8888888888888888,
              "#000019"
             ],
             [
              1,
              "#000020"
             ]
            ],
            "type": "contourcarpet"
           }
          ],
          "heatmap": [
           {
            "colorscale": [
             [
              0,
              "#000011"
             ],
             [
              0.1111111111111111,
              "#000012"
             ],
             [
              0.2222222222222222,
              "#000013"
             ],
             [
              0.3333333333333333,
              "#000014"
             ],
             [
              0.4444444444444444,
              "#000015"
             ],
             [
              0.5555555555555556,
              "#000016"
             ],
             [
              0.6666666666666666,
              "#000017"
             ],
             [
              0.7777777777777778,
              "#000018"
             ],
             [
              0.8888888888888888,
              "#000019"
             ],
             [
              1,
              "#000020"
             ]
            ],
            "type": "heatmap"
           }
          ],
          "histogram2d": [
           {
            "colorscale": [
             [
              0,
              "#000011"
             ],
             [
              0.1111111111111111,
              "#000012"
             ],
             [
              0.2222222222222222,
              "#000013"
             ],
             [
              0.3333333333333333,
              "#000014"
             ],
             [
              0.4444444444444444,
              "#000015"
             ],
             [
              0.5555555555555556,
              "#000016"
             ],
             [
              0.6666666666666666,
              "#000017"
             ],
             [
              0.7777777777777778,
              "#000018"
             ],
             [
              0.8888888888888888,
              "#000019"
             ],
             [
              1,
              "#000020"
             ]
            ],
            "type": "histogram2d"
           }
          ],
          "icicle": [
           {
            "textfont": {
             "color": "white"
            },
            "type": "icicle"
           }
          ],
          "sankey": [
           {
            "textfont": {
             "color": "#000036"
            },
            "type": "sankey"
           }
          ],
          "scatter": [
           {
            "marker": {
             "line": {
              "width": 0
             }
            },
            "type": "scatter"
           }
          ],
          "table": [
           {
            "cells": {
             "fill": {
              "color": "#000038"
             },
             "font": {
              "color": "#000037"
             },
             "line": {
              "color": "#000039"
             }
            },
            "header": {
             "fill": {
              "color": "#000040"
             },
             "font": {
              "color": "#000036"
             },
             "line": {
              "color": "#000039"
             }
            },
            "type": "table"
           }
          ],
          "waterfall": [
           {
            "connector": {
             "line": {
              "color": "#000036",
              "width": 2
             }
            },
            "decreasing": {
             "marker": {
              "color": "#000033"
             }
            },
            "increasing": {
             "marker": {
              "color": "#000032"
             }
            },
            "totals": {
             "marker": {
              "color": "#000034"
             }
            },
            "type": "waterfall"
           }
          ]
         },
         "layout": {
          "coloraxis": {
           "colorscale": [
            [
             0,
             "#000011"
            ],
            [
             0.1111111111111111,
             "#000012"
            ],
            [
             0.2222222222222222,
             "#000013"
            ],
            [
             0.3333333333333333,
             "#000014"
            ],
            [
             0.4444444444444444,
             "#000015"
            ],
            [
             0.5555555555555556,
             "#000016"
            ],
            [
             0.6666666666666666,
             "#000017"
            ],
            [
             0.7777777777777778,
             "#000018"
            ],
            [
             0.8888888888888888,
             "#000019"
            ],
            [
             1,
             "#000020"
            ]
           ]
          },
          "colorscale": {
           "diverging": [
            [
             0,
             "#000021"
            ],
            [
             0.1,
             "#000022"
            ],
            [
             0.2,
             "#000023"
            ],
            [
             0.3,
             "#000024"
            ],
            [
             0.4,
             "#000025"
            ],
            [
             0.5,
             "#000026"
            ],
            [
             0.6,
             "#000027"
            ],
            [
             0.7,
             "#000028"
            ],
            [
             0.8,
             "#000029"
            ],
            [
             0.9,
             "#000030"
            ],
            [
             1,
             "#000031"
            ]
           ],
           "sequential": [
            [
             0,
             "#000011"
            ],
            [
             0.1111111111111111,
             "#000012"
            ],
            [
             0.2222222222222222,
             "#000013"
            ],
            [
             0.3333333333333333,
             "#000014"
            ],
            [
             0.4444444444444444,
             "#000015"
            ],
            [
             0.5555555555555556,
             "#000016"
            ],
            [
             0.6666666666666666,
             "#000017"
            ],
            [
             0.7777777777777778,
             "#000018"
            ],
            [
             0.8888888888888888,
             "#000019"
            ],
            [
             1,
             "#000020"
            ]
           ],
           "sequentialminus": [
            [
             0,
             "#000011"
            ],
            [
             0.1111111111111111,
             "#000012"
            ],
            [
             0.2222222222222222,
             "#000013"
            ],
            [
             0.3333333333333333,
             "#000014"
            ],
            [
             0.4444444444444444,
             "#000015"
            ],
            [
             0.5555555555555556,
             "#000016"
            ],
            [
             0.6666666666666666,
             "#000017"
            ],
            [
             0.7777777777777778,
             "#000018"
            ],
            [
             0.8888888888888888,
             "#000019"
            ],
            [
             1,
             "#000020"
            ]
           ]
          },
          "colorway": [
           "#000001",
           "#000002",
           "#000003",
           "#000004",
           "#000005",
           "#000006",
           "#000007",
           "#000008",
           "#000009",
           "#000010"
          ]
         }
        },
        "title": {
         "text": "Habilidades que precisam ser melhoradas"
        },
        "xaxis": {
         "anchor": "y",
         "domain": [
          0,
          1
         ],
         "title": {
          "text": "Habilidade"
         }
        },
        "yaxis": {
         "anchor": "x",
         "domain": [
          0,
          1
         ],
         "title": {
          "text": "Percentual de Acerto"
         }
        }
       }
      },
      "image/png": "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"
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "diag_habilidades_abaixo = diagnostica[diagnostica[\"HABILIDADE - FAIXA\"].isin([\"Baixo\", \"Médio Baixo\"])]\n",
    "diag_habilidades_abaixo = diag_habilidades_abaixo.sort_values(\"HABILIDADE - ACERTO %\")\n",
    "fig = px.bar(\n",
    "    diag_habilidades_abaixo,\n",
    "    x=\"HABILIDADE - DESCRIÇÃO\",\n",
    "    y=\"HABILIDADE - ACERTO %\",\n",
    "    color=\"HABILIDADE - FAIXA\",\n",
    "    title=\"Habilidades que precisam ser melhoradas\",\n",
    "    text=\"HABILIDADE - ACERTO %\"\n",
    ")\n",
    "\n",
    "fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')\n",
    "fig.update_layout(xaxis_title=\"Habilidade\", yaxis_title=\"Percentual de Acerto\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "8e0973b5-a080-49fa-9472-a0652b00d8dd",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-11-26 13:21:35.996 Please replace `use_container_width` with `width`.\n",
      "\n",
      "`use_container_width` will be removed after 2025-12-31.\n",
      "\n",
      "For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.\n",
      "2025-11-26 13:21:36.002 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-26 13:21:36.004 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-26 13:21:36.006 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-26 13:21:36.607 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\patri\\miniconda3\\envs\\p_caetano\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n",
      "2025-11-26 13:21:36.607 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-11-26 13:21:36.607 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "st.plotly_chart(fig, use_container_width=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1f1b4c0a-af73-4799-ac89-fcd71c94d7af",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (p_caetano)",
   "language": "python",
   "name": "p_caetano"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.14"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
