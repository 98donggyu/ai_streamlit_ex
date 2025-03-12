# import streamlit as st
# import pandas as pd
# import numpy as np

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
# print(chart_data)
# st.line_chart(chart_data)

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    np.random.randn(20, 3), columns=["col1", "col2", "col3"]
)

st.line_chart(
    chart_data,
    x="col1",
    y=["col2", "col3"],
    color=["#006021", "#0000FF"],  # Optional
)

