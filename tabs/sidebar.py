import streamlit as st

def sidebar():
    st.sidebar.image("images/logo.png")

# Add instructions on how to use the app to the sidebar
    st.sidebar.header("How to use LINDDUN GPT")
    if "keys" not in st.session_state:
        st.session_state["keys"] = {}

    with st.sidebar:
        try:
            openai_api_key = st.secrets["openai_api_key"]
            st.session_state["keys"]["openai_api_key"] = openai_api_key
            google_api_key = st.secrets["google_api_key"]
            st.session_state["keys"]["google_api_key"] = google_api_key
            mistral_api_key = st.secrets["mistral_api_key"]
            st.session_state["keys"]["mistral_api_key"] = mistral_api_key
        except Exception as e:
            openai_api_key = None
            google_api_key = None
            mistral_api_key = None
        # Add model selection input field to the sidebar
        model_provider = st.selectbox(
            "Select your preferred model provider:",
            [
                "OpenAI API",
                "Google AI API",
                "Mistral API",
            ],  # ["OpenAI API", "Azure OpenAI Service", "Google AI API", "Mistral API"],
            key="model_provider",
            help="Select the model provider you would like to use. This will determine the models available for selection.",
        )
        st.markdown(
                """
        1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys), [Google AI API key](https://makersuite.google.com/app/apikey) and/or [Mistral API key](https://console.mistral.ai/api-keys/) below
        2. Choose the models you would like to use for each provider
        3. Provide details of the application that you would like to privacy threat model
        4. Generate a privacy threat model, or simulate the LINDDUN Go methodology for your application (even with multiple LLMs having a discussion)
        """
            )
        c1, c2 = st.columns([1, 1])

        with c1:
            openai_api_key_input = st.text_input(
                "Enter your OpenAI API key:",
                type="password",
                help="You can find your OpenAI API key on the [OpenAI dashboard](https://platform.openai.com/account/api-keys).",
            )
            if openai_api_key_input:
                openai_api_key = openai_api_key_input
            st.session_state["keys"]["openai_api_key"] = openai_api_key

            google_api_key_input = st.text_input(
                "Enter your Google AI API key:",
                type="password",
                help="You can generate a Google AI API key in the [Google AI Studio](https://makersuite.google.com/app/apikey).",
            )
            if google_api_key_input:
                google_api_key = google_api_key_input
            st.session_state["keys"]["google_api_key"] = google_api_key

        with c2:
            mistral_api_key_input = st.text_input(
                "Enter your Mistral API key:",
                type="password",
                help="You can generate a Mistral API key in the [Mistral console](https://console.mistral.ai/api-keys/).",
            )
            if mistral_api_key_input:
                mistral_api_key = mistral_api_key_input
            st.session_state["keys"]["mistral_api_key"] = mistral_api_key
            st.empty()

        if model_provider == "Azure OpenAI Service":
            st.markdown(
                """
        1. Enter your Azure OpenAI API key, endpoint and deployment name below 🔑
        2. Provide details of the application that you would like to threat model  📝
        3. Generate a threat list, attack tree and/or mitigating controls for your application 🚀
        """
            )

            # Add Azure OpenAI API key input field to the sidebar
            azure_api_key = st.text_input(
                "Azure OpenAI API key:",
                type="password",
                help="You can find your Azure OpenAI API key on the [Azure portal](https://portal.azure.com/).",
            )
            st.session_state["keys"]["azure_api_key"] = azure_api_key

            # Add Azure OpenAI endpoint input field to the sidebar
            azure_api_endpoint = st.text_input(
                "Azure OpenAI endpoint:",
                help="Example endpoint: https://YOUR_RESOURCE_NAME.openai.azure.com/",
            )
            st.session_state["azure_api_endpoint"] = azure_api_endpoint

            # Add Azure OpenAI deployment name input field to the sidebar
            azure_deployment_name = st.text_input(
                "Deployment name:",
            )
            st.session_state["azure_deployment_name"] = azure_deployment_name

            st.info("Please note that you must use an 1106-preview model deployment.")

            azure_api_version = "2023-12-01-preview"  # Update this as needed
            st.session_state["azure_api_version"] = azure_api_version

            st.write(f"Azure API Version: {azure_api_version}")

        c1, c2 = st.columns([1, 1])
        with c1:
            # Add model selection input field to the sidebar
            openai_model = st.selectbox(
                "OpenAI model:",
                ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4", "gpt-4o"],
                key="openai_model",
                help="OpenAI have moved to continuous model upgrades so `gpt-3.5-turbo`, `gpt-4` and `gpt-4-turbo` point to the latest available version of each model.",
            )
            # Add model selection input field to the sidebar
            google_model = st.selectbox(
                "Google AI model:",
                ["gemini-1.5-pro-latest"],
                key="google_model",
            )
        with c2:
            # Add model selection input field to the sidebar
            mistral_model = st.selectbox(
                "Mistral model:",
                ["mistral-large-latest", "mistral-small-latest", "open-mixtral-8x22b"],
                key="mistral_model",
            )

        st.markdown("""---""")
        st.slider("Temperature setting", 0.01, 1.0, 0.7, key="temperature", help="The randomness of the model's responses. Lower values are more deterministic, higher values are more random.")

# Add "About" section to the sidebar
    st.sidebar.header("About")

    with st.sidebar:
        st.markdown(
            """Welcome to LINDDUN GPT, an AI-powered tool designed to help developers
        in privacy threat modelling for their applications, using the [LINDDUN](https://linddun.org/) methodology."""
        )
        st.markdown(
            """Privacy threat modelling is a key activity in the software development
            lifecycle, but is often overlooked or poorly executed. LINDDUN GPT aims
                to help teams produce more comprehensive threat models by
                leveraging the power of Large Language Models (LLMs) to generate a
                threat list for an
        application based on the details provided, analyzing threats specified by the LINDDUN scheme."""
        )
        st.markdown("""---""")


# Add "Example Application Description" section to the sidebar
    st.sidebar.header("Example Application Description")

    with st.sidebar:
        st.markdown(
            "Below is an example application description that you can use to test LINDDUN GPT:"
        )
        st.code(
            """
            A web application that 
            allows users to create, store, and share
            personal notes. The application is built using the React frontend
            framework and a Node.js backend with a MongoDB database. Users can
            sign up for an account and log in using OAuth2 with Google or
            Facebook. The notes are encrypted at rest and are only accessible
            by the user who created them. The application also supports
            real-time collaboration on notes with other users.
            """,
            language="md"
        )
        st.markdown(
            "Additionally, this is an example for the data policy section that works with the example application and highlights some possible issues:"
        )
        st.code(
            """
            The application stores 
            user data in a MongoDB database. Users can
            access, modify, or delete their data by logging into their account.
            The data retention policy specifies that user data is stored for 2
            years after account deletion, after which it is permanently deleted.
            The application uses encryption to protect user data at rest and in
            transit. User data is never shared with third parties without user
            consent, except for advertising purposes.
            """,
            language="md"
        )
        st.markdown("""---""")

# Add "FAQs" section to the sidebar
    st.sidebar.header("FAQs")

#with st.sidebar: