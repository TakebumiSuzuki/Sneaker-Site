<script setup>


</script>


<template>

    <!-- <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .glass {
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .glass:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        .gradient-border {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
            padding: 2px;
            border-radius: 8px;
        }
        .gradient-border > div {
            background: white;
            border-radius: 6px;
        }
        .gradient-border:hover > div {
            background: #f8f9fa;
        }
        .neon {
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        }
        .neon:hover {
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.8);
        }
        .floating {
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
        }
    </style>
</head> -->
<div class="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 min-h-screen p-8">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-bold text-white mb-12 text-center">モダンなTailwind CSSボタン</h1>

        <!-- 基本的なボタン -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">基本的なボタン</h2>
            <div class="flex flex-wrap gap-4">
                <!-- プライマリボタン -->
                <button class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Primary Button
                </button>

                <!-- セカンダリボタン -->
                <button class="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Secondary Button
                </button>

                <!-- アウトラインボタン -->
                <button class="px-6 py-3 border-2 border-white text-white font-semibold rounded-lg transition-all duration-200 hover:bg-white hover:text-gray-900 transform hover:scale-105 active:scale-95">
                    Outline Button
                </button>
            </div>
        </section>

        <!-- グラデーションボタン -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">グラデーションボタン</h2>
            <div class="flex flex-wrap gap-4">
                <!-- グラデーション1 -->
                <button class="px-6 py-3 bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg">
                    Pink Gradient
                </button>

                <!-- グラデーション2 -->
                <button class="px-6 py-3 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg">
                    Purple Gradient
                </button>

                <!-- グラデーション3 -->
                <button class="px-6 py-3 bg-gradient-to-r from-green-400 to-blue-500 hover:from-green-500 hover:to-blue-600 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg">
                    Ocean Gradient
                </button>
            </div>
        </section>

        <!-- ネオンボタン -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">ネオンボタン</h2>
            <div class="flex flex-wrap gap-4">
                <button class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-300 neon">
                    Neon Blue
                </button>

                <button class="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-all duration-300 shadow-[0_0_20px_rgba(147,51,234,0.5)] hover:shadow-[0_0_30px_rgba(147,51,234,0.8)]">
                    Neon Purple
                </button>

                <button class="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-all duration-300 shadow-[0_0_20px_rgba(34,197,94,0.5)] hover:shadow-[0_0_30px_rgba(34,197,94,0.8)]">
                    Neon Green
                </button>
            </div>
        </section>

        <!-- グラスモーフィズム -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">グラスモーフィズム</h2>
            <div class="flex flex-wrap gap-4">
                <button class="px-6 py-3 glass text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Glass Button
                </button>

                <button class="px-6 py-3 backdrop-blur-sm bg-white/20 border border-white/30 hover:bg-white/30 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Frosted Glass
                </button>
            </div>
        </section>

        <!-- 3Dボタン -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">3Dボタン</h2>
            <div class="flex flex-wrap gap-4">
                <button class="px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-all duration-200 shadow-[0_6px_0_0_#dc2626] hover:shadow-[0_4px_0_0_#dc2626] transform hover:translate-y-1 active:translate-y-2 active:shadow-[0_2px_0_0_#dc2626]">
                    3D Button
                </button>

                <button class="px-6 py-3 bg-yellow-500 hover:bg-yellow-600 text-white font-semibold rounded-lg transition-all duration-200 shadow-[0_6px_0_0_#eab308] hover:shadow-[0_4px_0_0_#eab308] transform hover:translate-y-1 active:translate-y-2 active:shadow-[0_2px_0_0_#eab308]">
                    3D Yellow
                </button>
            </div>
        </section>

        <!-- 特殊エフェクト -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">特殊エフェクト</h2>
            <div class="flex flex-wrap gap-4">
                <!-- グラデーションボーダー -->
                <div class="gradient-border">
                    <div class="px-6 py-3 rounded-lg transition-all duration-200">
                        <span class="text-gray-800 font-semibold">Gradient Border</span>
                    </div>
                </div>

                <!-- フローティング -->
                <button class="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-200 floating shadow-lg">
                    Floating Button
                </button>

                <!-- リップル効果 -->
                <button class="px-6 py-3 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-lg transition-all duration-200 relative overflow-hidden group">
                    <span class="relative z-10">Ripple Effect</span>
                    <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 transition-opacity duration-300 rounded-lg"></div>
                </button>
            </div>
        </section>

        <!-- アイコン付きボタン -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">アイコン付きボタン</h2>
            <div class="flex flex-wrap gap-4">
                <button class="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                    </svg>
                    Add Item
                </button>

                <button class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                    Delete
                </button>

                <button class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"/>
                    </svg>
                    Download
                </button>
            </div>
        </section>

        <!-- サイズバリエーション -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">サイズバリエーション</h2>
            <div class="flex flex-wrap items-center gap-4">
                <button class="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Small
                </button>

                <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Medium
                </button>

                <button class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white text-lg font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Large
                </button>

                <button class="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white text-xl font-semibold rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Extra Large
                </button>
            </div>
        </section>

        <!-- 状態バリエーション -->
        <section class="mb-12">
            <h2 class="text-2xl font-semibold text-white mb-6">状態バリエーション</h2>
            <div class="flex flex-wrap gap-4">
                <button class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95">
                    Normal
                </button>

                <button class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center gap-2" disabled>
                    <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Loading...
                </button>

                <button class="px-6 py-3 bg-gray-400 text-gray-200 font-semibold rounded-lg cursor-not-allowed opacity-50" disabled>
                    Disabled
                </button>

                <button class="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                    Success
                </button>
            </div>
        </section>
    </div>
</div>





</template>