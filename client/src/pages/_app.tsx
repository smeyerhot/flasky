import { AppProps } from "next/app";

import '../styles/index.css'
const App = ({
  Component,
  pageProps,
}: AppProps): React.ReactElement => <Component {...pageProps} />;

export default App;