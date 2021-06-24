## Report

### Dataset

BlackFriday.csv

### Dashboard

#### Graph1

##### Scatter: Graph of categories and purchase based on age

Filter: Age

x: Product_Category_1

y: Purchase

```python
def update_graph(age_value):

    dff = df[df['Age'] == age_value]
    return {
        'data': [go.Scatter(
            x=dff['Product_Category_1'],
            y=dff['Purchase'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Product_Category_1'
                #'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'Purchase'
                #'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }

```

#### Graph2

##### Series: Graph of User_ID and purchase based on age and product category1

Filter: Age, Product_Category_1

x: User_ID

y: Purchase

```python
def series(age_value, procate_value):
                 
    dff = df[df['Age'] == age_value]
    dff_procate = dff[dff['Product_Category_1']==procate_value]
    return {
        'data': [go.Scatter(
            x=dff_procate['User_ID'],
            y=dff_procate['Purchase'],
      
            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'User_ID'
            },
            yaxis={
                'title': 'Purchase'
         
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }
```

#### Graph3

##### Pie: Rate of gender based on product category

Filter: Product_Category_1

labels: Gender

```python
def create_gender_pie(pro_cate):
    dff_cate = df[df['Product_Category_1'] == pro_cate]
    # total = df.shape[0]
    counts = dff_cate['Gender'].value_counts(ascending=True,normalize=True).tolist()
    # print(counts)
    # print(counts[0])
    # print(counts[1])

    return {
        'data': [go.Pie(
            labels=['F','M'],
            values=[counts[0],counts[1]]
        )]
        
    }
```



## Readme

 Running on http://127.0.0.1:8060/