interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_ACCESS_TOKEN_EXPIRE: string;
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }