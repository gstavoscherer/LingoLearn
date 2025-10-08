<script lang="ts">
    import type { Snippet } from 'svelte';

    let { children }:{ children: Snippet } = $props();
</script>

<div class="layout">
    {@render children()}
</div>

<svelte:head>
    <style>
        body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
            background-color: #f8f9fa;
            display: flex;
            justify-content:center;
            align-items:center;
        }

        .auth-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .auth-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            width: 100%;
            max-width: 420px;
            padding: 40px;
        }

        .auth-header {
            text-align: center;
            margin-bottom: 32px;
        }

        .auth-header h1 {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .auth-header p {
            color: #7f8c8d;
            font-size: 14px;
            margin: 0;
        }

        .auth-form {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .input-group label {
            font-size: 14px;
            color: #2c3e50;
            font-weight: 500;
        }

        input {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s ease;
            background-color: #f6f6f6;
        }

        input:focus {
            border-color: #4c7ede;
            box-shadow: 0 0 0 3px rgba(76, 126, 222, 0.2);
            outline: none;
            background-color: white;
        }

        .auth-button {
            background-color: #4c7ede;
            color: white;
            border: none;
            width: 80%;
            padding: 14px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            align-self:center;
            transition: background-color 0.3s ease;
            margin-top: 8px;
        }

        .auth-button:hover {
            background-color: #3a6bc8;
        }

        .forgot-password {
            text-align: right;
            font-size: 12px;
            color: #7f8c8d;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .forgot-password:hover {
            color: #4c7ede;
        }

        .signup-section {
            text-align: center;
            margin-top: 24px;
            font-size: 14px;
            color: #7f8c8d;
        }

        .signup-link {
            color: #4c7ede;
            font-weight: 500;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .signup-link:hover {
            color: #3a6bc8;
            text-decoration: underline;
        }

        .error-message {
            background-color: #ffe0e0;
            color: #c0392b;
            border: 1px solid #e74c3c;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 14px;
            align-self: center;
            width: 80%;
        }
    </style>
</svelte:head>
