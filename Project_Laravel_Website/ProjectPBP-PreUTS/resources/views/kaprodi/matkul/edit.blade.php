{{-- @extends('layouts.app') --}}
@include('../header')
<x-navbar/>
{{-- @section('content') --}}
<div class="flex flex-col flex-grow">
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
        <div class="max-w-lg mx-auto bg-white border border-gray-200 rounded-lg shadow-md p-8">
            <h1 class="text-3xl font-semibold mb-6 text-gray-800">Update Matakuliah</h1>
            
            <form action="{{ route('matkul.update', $matkul->kode_mk) }}" method="POST">

                @csrf
                @method('PUT') <!-- Tambahkan ini untuk method PUT -->
                
                <!-- NIM Input -->
                <div class="mb-4">
                    <label for="kodemk" class="block mb-2 text-sm font-medium text-gray-900">Kode Matakuliah</label>
                    <input 
                        type="text" 
                        name="kode_mk" 
                        id="kodemk" 
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        value="{{ $matkul->kode_mk }}">
                    @error('kode_mk')
                        <span class="text-red-500 text-sm mt-1">{{ $message }}</span>
                    @enderror
                </div>

                <!-- Nama Input -->
                <div class="mb-4">
                    <label for="nama" class="block mb-2 text-sm font-medium text-gray-900">Nama Matakuliah</label>
                    <input 
                        type="text" 
                        name="nama_mk" 
                        id="nama" 
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        value="{{ ( $matkul->nama_mk ) }}">
                    @error('nama_mk')
                        <span class="text-red-500 text-sm mt-1">{{ $message }}</span>
                    @enderror
                </div>

                <!-- Email Input -->
                <div class="mb-4">
                    <label for="semester" class="block mb-2 text-sm font-medium text-gray-900">Semester</label>
                    <input 
                        type="number" 
                        name="semester" 
                        id="semester" 
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        value="{{ ( $matkul->semester ) }}">
                    @error('semester')
                        <span class="text-red-500 text-sm mt-1">{{ $message }}</span>
                    @enderror
                </div>

                <div class="mb-4">
                    <label for="sks" class="block mb-2 text-sm font-medium text-gray-900">SKS</label>
                    <input 
                        type="number" 
                        name="sks" 
                        id="sks" 
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        value="{{ ( $matkul -> sks ) }}">
                    @error('sks')
                        <span class="text-red-500 text-sm mt-1">{{ $message }}</span>
                    @enderror
                </div>

                <div class="mb-4">
                    <label for="kurikulum" class="block mb-2 text-sm font-medium text-gray-900">Kurikulum</label>
                    <input 
                        type="text" 
                        name="kurikulum" 
                        id="kurikulum" 
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        value="{{ ($matkul->kurikulum) }}">
                    @error('kurikulum')
                        <span class="text-red-500 text-sm mt-1">{{ $message }}</span>
                    @enderror
                </div>

                <div class="mb-4">
                    <label for="kodeprodi" class="block mb-2 text-sm font-medium text-gray-900">Kode Prodi</label>
                    <input 
                        type="text" 
                        name="kode_prodi" 
                        id="kode_prodi" 
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        value="{{ ($matkul->kode_prodi) }}">
                    @error('kode_prodi')
                        <span class="text-red-500 text-sm mt-1">{{ $message }}</span>
                    @enderror
                </div>

                <div class="mb-4">
                    <label for="sifat" class="block mb-2 text-sm font-medium text-gray-900">Sifat</label>
                    <input 
                        type="text" 
                        name="sifat" 
                        id="sifat" 
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        value="{{ ($matkul->sifat) }}">
                    @error('sifat')
                        <span class="text-red-500 text-sm mt-1">{{ $message }}</span>
                    @enderror
                </div>

                <!-- Submit Button -->
                <div>
                    <button type="submit" class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5">
                        Update
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
    
@include('../footer')
{{-- @endsection --}}
