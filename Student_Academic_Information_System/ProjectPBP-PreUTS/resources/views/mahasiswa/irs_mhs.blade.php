@include('header')
<div class="flex flex-col min-h-screen">
    <!-- NavBar -->
    <x-navbar/>
    <div class="flex flex-col flex-grow">
        <!-- Header -->
        <div class="flex items-center justify-between py-3 p-8">
            <div class="font-bold text-lg md:text-xl pl-4 py-1">
                IRS
            </div>
        </div>

        <!-- Content -->
        <div class="flex py-3 p-8">
            <!-- SideBar Information -->
            <div class="flex flex-col pl-4 w-1/4 gap-5">
                <!-- Info Mahasiswa -->
                <div class="p-5 border-2 border-[#80747475] rounded-lg gap-3 shadow-[0_2px_4px_rgba(0,0,0,0.1)]">
                    <p class="font-bold">Nama : </p>
                    <p>{{ Auth::user()->mahasiswa->nama }}</p>
                    <p class="font-bold">NIM : </p>
                    <p>{{ Auth::user()->mahasiswa->nim }}</p>
                    <p class="font-bold">Tahun Akademik : </p>
                    <p>{{ $latestIrs->tahun->tahun_akademik }} ({{Auth::user()->mahasiswa->semester % 2 != 0 ? 'Ganjil' : 'Genap'}})</p>
                    <p class="font-bold">Semester : </p>
                    <p>{{ Auth::user()->mahasiswa->semester }}</p>
                    <p class="font-bold">IPK : </p>
                    <p>{{ Auth::user()->mahasiswa->ipk }}</p>
                </div>

                <!-- Menampilkan Mata Kuliah Wajib -->
                <div class="p-5 border-2 border-[#80747475] rounded-lg gap-3 shadow-[0_2px_4px_rgba(0,0,0,0.1)]">
                    <h2 class="text-lg font-bold mb-4">Mata kuliah wajib semester ini</h2>
                    <div class="flex flex-col my-3">
                        <div class="flex flex-col overflow-y-auto max-h-60 gap-3">
                            @foreach ($mataKuliah as $mkwajib)
                                <div class="rounded p-2 border-l-2 border-purple-600 bg-purple-50">
                                    <div class="flex justify-between items-center">
                                        <p class="text-sm font-normal text-gray-900 mb-px max-w-24">{{ $mkwajib->nama_mk }}</p>
                                        <div class="flex flex-col text-right">
                                            <p class="text-sm font-normal text-gray-600 mb-px">Semester: {{ $mkwajib->semester }}</p>
                                            <p class="text-sm font-normal text-gray-600 mb-px">SKS: {{ $mkwajib->sks }}</p>
                                        </div>
                                    </div>
                                </div>
                            @endforeach
                        </div>
                    </div>
                </div>
                
            <!-- Mata Kuliah Tambahan -->
            <div class="p-5 border-2 border-[#80747475] rounded-lg gap-3 shadow-[0_2px_4px_rgba(0,0,0,0.1)] min-h-80">
                <h2 class="text-lg font-bold mb-4">Tambah Mata kuliah</h2>
                <div class="flex items-center">
                    <div id="search_mk" class="mt-2 rounded-md bg-white w-full">
                        <div class="relative group">
                            <!-- Search input -->
                            <input 
                                id="search-input" 
                                class="w-full px-4 py-2 text-gray-800 border rounded-md border-gray-300" 
                                type="text" 
                                placeholder="Cari mata kuliah ..."
                                autocomplete="off"
                            >
                            <!-- Dropdown -->
                            <div 
                                id="dropdown" 
                                class="hidden absolute bg-white border border-gray-300 w-full z-10 max-h-40 overflow-y-auto rounded-md shadow-md">
                                @foreach ($mkTambahan as $mk)
                                    <a  
                                        href="#" 
                                        data-id="{{ $mk->kode_mk }}" 
                                        class="block px-4 py-2 text-gray-700 hover:bg-gray-100 cursor-pointer add-mk">
                                        {{ $mk->nama_mk }} - Semester {{ $mk->semester }}
                                    </a>
                                @endforeach
                            </div>                                
                        </div>
                    </div>
                </div>

                <!-- Tombol Simpan Jadwal -->
                <div class="mt-4">
                    <button 
                        id="save-button" 
                        class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
                    >
                        Tambah mata kuliah
                    </button>
                </div>

                <!-- Mata kuliah yang ditambahkan -->
                <div class="flex flex-col my-3">
                    <div class="flex flex-col overflow-y-auto max-h-60 gap-3">
                        @foreach ($selectedMKs as $mk)
                        <div class="rounded p-2 border-l-2 border-purple-600 bg-purple-50">
                            <div class="flex justify-between items-center">
                                <div>
                                    <p class="text-sm font-normal text-gray-900 mb-px max-w-40">{{ $mk['nama_mk'] }}</p>
                                </div>
                                <div class="flex gap-3">
                                    <div class="flex flex-col text-right">
                                        <p class="text-sm font-normal text-gray-600 mb-px">Semester: {{ $mk['semester'] }}</p>
                                        <p class="text-sm font-normal text-gray-600 mb-px">SKS: {{ $mk['sks'] }}</p>
                                    </div>                                
                                    <button class="remove-mk text-red-500 hover:text-red-700" data-id="{{ $mk['kode_mk'] }}">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                        @endforeach
                    </div>
                </div>
            </div>
            </div>


            <!-- IRS Calendar -->
            <div class="mx-5">
                <section class="relative border-2 border-[#80747475] rounded-lg gap-3 shadow-[0_2px_4px_rgba(0,0,0,0.1)]">
                    <div class="w-full max-w-7xl mx-auto px-6 lg:px-8 overflow-x-auto">
                        <!-- Row Hari -->
                        <div class=" relative">
                            <div class="grid grid-cols-6 border-t border-r border-gray-200 sticky top-0 left-0 w-full">
                                <div class="p-3.5 flex items-center justify-center text-sm font-medium  text-gray-900"></div>
                                <div class="p-3.5 flex items-center justify-center text-sm font-medium  text-gray-900">Senin</div>
                                <div class="p-3.5 flex items-center justify-center text-sm font-medium  text-gray-900">Selasa</div>
                                <div class="p-3.5 flex items-center justify-center text-sm font-medium  text-gray-900">Rabu</div>
                                <div class="p-3.5 flex items-center justify-center text-sm font-medium  text-gray-900">kamis</div>
                                <div class="p-3.5 flex items-center justify-center text-sm font-medium  text-gray-900">Jum'at</div>
                            </div>
                        <!-- Jadwal -->
                        <div class="hidden grid-cols-6 sm:grid w-full overflow-x-auto">
                            <!-- Row Jam 06.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5 border-t border-r border-gray-200 flex items-center justify-center transition-all">
                                <span class="text-xs font-semibold text-gray-400">06:00 am</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['06:00:00', '06:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['06:00:00', '06:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['06:00:00', '06:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['06:00:00', '06:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['06:00:00', '06:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>

                            <!-- Row Jam 07.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5 border-t border-r border-gray-200 flex items-center justify-center transition-all">
                                <span class="text-xs font-semibold text-gray-400">07:00 am</span>
                            </div>
                                    <!-- Senin -->
                                    <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                        @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['07:00:00', '07:59:59']) as $jadwal)
                                        <form action="{{ route('irs.add') }}" method="POST">
                                            @csrf
                                            <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                            <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                            <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                                <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                    <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                    <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                    <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                                </div>
                                            </button>
                                        </form> 
                                        @endforeach
                                    </div>
                                    <!-- Selasa -->
                                    <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                        @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['07:00:00', '07:59:59']) as $jadwal)
                                        <form action="{{ route('irs.add') }}" method="POST">
                                            @csrf
                                            <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                            <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                            <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                                <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                    <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                    <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                    <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                                </div>
                                            </button>
                                        </form> 
                                        @endforeach
                                    </div>
                                    <!-- Rabu -->
                                    <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                        @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['07:00:00', '07:59:59']) as $jadwal)
                                        <form action="{{ route('irs.add') }}" method="POST">
                                            @csrf
                                            <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                            <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                            <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                                <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                    <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                    <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                    <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                                </div>
                                            </button>
                                        </form> 
                                        @endforeach
                                    </div>
                                    <!-- Kamis -->
                                    <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                        @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['07:00:00', '07:59:59']) as $jadwal)
                                        <form action="{{ route('irs.add') }}" method="POST">
                                            @csrf
                                            <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                            <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                            <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                                <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                    <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                    <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                    <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                                </div>
                                            </button>
                                        </form> 
                                        @endforeach
                                    </div>
                                    <!-- Jumat -->
                                    <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                        @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['07:00:00', '07:59:59']) as $jadwal)
                                        <form action="{{ route('irs.add') }}" method="POST">
                                            @csrf
                                            <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                            <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                            <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                                <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                    <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                    <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                    <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                                </div>
                                            </button>
                                        </form> 
                                        @endforeach
                                    </div>
                            
                            
                            <!-- Row Jam 08.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">08:00 am</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['08:00:00', '08:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['08:00:00', '08:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['08:00:00', '08:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['08:00:00', '08:59:59'])  as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['08:00:00', '08:59:59'])  as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                            
                            <!-- Row Jam 09.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">09:00 am</span>
                            </div>
                                    <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['09:00:00', '09:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['09:00:00', '09:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['09:00:00', '09:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['09:00:00', '09:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['09:00:00', '09:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                        
                            
                            <!-- Row Jam 10.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">10:00 am</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['10:00:00', '10:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['10:00:00', '10:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['10:00:00', '10:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['10:00:00', '10:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['10:00:00', '10:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                            
                            <!-- Row Jam 11.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">11:00 am</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['11:00:00', '11:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['11:00:00', '11:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['11:00:00', '11:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['11:00:00', '11:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['11:00:00', '11:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                
                            <!-- Row Jam 12.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">12:00 pm</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['12:00:00', '12:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['12:00:00', '12:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['12:00:00', '12:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['12:00:00', '12:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['12:00:00', '12:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>

                            <!-- Row Jam 13.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">13:00 pm</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['13:00:00', '13:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form>                                    
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['13:00:00', '13:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['13:00:00', '13:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['13:00:00', '13:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['13:00:00', '13:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>

                            <!-- Row Jam 14.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">14:00 pm</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['14:00:00', '14:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['14:00:00', '14:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['14:00:00', '14:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['14:00:00', '14:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['14:00:00', '14:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>


                            <!-- Row Jam 15.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">15:00 pm</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['15:00:00', '15:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['15:00:00', '15:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['15:00:00', '15:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['15:00:00', '15:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['15:00:00', '15:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>

                            <!-- Row Jam 16.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">16:00 pm</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['16:00:00', '16:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['16:00:00', '16:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['16:00:00', '16:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['16:00:00', '16:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['16:00:00', '16:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>

                            <!-- Row Jam 17.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">17:00 pm</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['17:00:00', '17:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['17:00:00', '17:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['17:00:00', '17:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['17:00:00', '17:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['17:00:00', '17:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                
                            <!-- Row Jam 18.00 -->
                            <div class="h-auto min-h-32 p-0.5 md:p-3.5 border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                <span class="text-xs font-semibold text-gray-400">18:00 pm</span>
                            </div>
                                <!-- Senin -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Senin')->whereBetween('jam_mulai', ['18:00:00', '18:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Selasa -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Selasa')->whereBetween('jam_mulai', ['18:00:00', '18:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Rabu -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Rabu')->whereBetween('jam_mulai', ['18:00:00', '18:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Kamis -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 transition-all ">
                                    @foreach ($jadwals->where('hari', 'Kamis')->whereBetween('jam_mulai', ['18:00:00', '18:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                                <!-- Jumat -->
                                <div class="h-auto min-h-32 p-0.5 md:p-3.5   border-t border-r border-gray-200 flex items-center justify-center transition-all ">
                                    @foreach ($jadwals->where('hari', 'Jumat')->whereBetween('jam_mulai', ['18:00:00', '18:59:59']) as $jadwal)
                                    <form action="{{ route('irs.add') }}" method="POST">
                                        @csrf
                                        <input type="hidden" name="id_jadwal" value="{{ $jadwal->id_jadwal }}">
                                        <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                        <button type="submit" class="w-full text-left hover:bg-purple-100 transition">
                                            <div class="rounded m-2 p-2 border-l-2 border-purple-600 bg-purple-50">
                                                <p class="text-xs font-normal text-gray-900 mb-px">{{ $jadwal->mataKuliah->nama_mk }} ({{ $jadwal->kode_kelas }})</p>
                                                <p class="text-xs font-semibold text-purple-600">{{ \Carbon\Carbon::parse($jadwal->jam_mulai)->format('H:i') }} - {{ \Carbon\Carbon::parse($jadwal->jam_selesai)->format('H:i') }}</p>
                                                <p class="text-xs font-normal text-gray-600">Ruang: {{ $jadwal->ruang }}</p>
                                            </div>
                                        </button>
                                    </form> 
                                    @endforeach
                                </div>
                        </div>  
                </section>                              
            </div>

            <!-- Sidebar Container -->
            <div class="relative">
                <!-- Sidebar (Fixed) -->
                <aside class="fixed right-0 rounded-lg w-36 bg-gradient-to-r from-red-500 to-red-700 shadow-xl text-white">
                    <div class="p-4">
                        <div class="flex justify-center">
                            <h2 class="font-bold text-lg text-center">Total SKS</h2>
                        </div>
                    </div>
                    <div class="bg-white text-gray-800 rounded-b-lg p-4 mt-1 flex flex-col items-center">
                        <p class="font-bold text-lg">
                            {{ $totalSKS }}
                        </p>
                        <button id="viewDetailsBtn" class="w-full mt-4 py-2 px-3 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium shadow-md">
                            Lihat Detail
                        </button>
                    </div>
                </aside>

                <!-- Slide-in Sidebar -->
                <div id="detailsSidebar" class="fixed top-0 right-0 h-full w-96 bg-white shadow-xl transform translate-x-full transition-transform duration-300">
                    <div class="flex justify-between items-center px-6 py-4 border-b bg-gradient-to-r from-red-500 to-red-700 text-white">
                        <h2 class="text-xl font-semibold">Detail IRS</h2>
                        <button id="closeSidebarBtn" class="text-xl font-bold hover:text-gray-200">&times;</button>
                    </div>
                    <div class="p-6">
                        <div class="detail-irs mt-4">
                            <div class="">
                                <h3 class="text-lg font-semibold text-gray-800 border-b pb-2">List Mata Kuliah </h3>
                                <p>SKS Terpilih = {{ $totalSKS }}</p>
                            </div>
                            <ul class="mt-4 space-y-3 max-h-96 overflow-y-auto">
                                @foreach ($detailIrs as $detail)
                                    <li class="flex justify-between items-center bg-gray-100 p-3 rounded-lg shadow-sm hover:bg-gray-200">
                                        <div>
                                            <p class="font-medium text-gray-900">{{ $detail->jadwal->mataKuliah->nama_mk }} ({{ $detail->jadwal->kode_kelas }})</p>
                                            <p class="text-sm text-gray-600">{{ $detail->jadwal->kode_mk }}</p>
                                            <p class="text-sm text-gray-600">
                                                {{ \Carbon\Carbon::parse($detail->jadwal->jam_mulai)->format('H:i') }} - 
                                                {{ \Carbon\Carbon::parse($detail->jadwal->jam_selesai)->format('H:i') }} 
                                                
                                            </p>
                                            <p class="text-sm text-gray-600">{{ $detail->jadwal->mataKuliah->sks }} SKS</p>
                                        </div>
                                        <form action="{{ route('irs.delete') }}" method="POST" style="display:inline;">
                                            @csrf
                                            @method('DELETE')
                                            <input type="hidden" name="id_jadwal" value="{{ $detail->jadwal->id_jadwal }}">
                                            <input type="hidden" name="id_irs" value="{{ $irs->id_irs }}">
                                            <button type="submit" class="alert-delete bg-red-500 hover:bg-red-600 text-white px-3 py-1 text-sm rounded-lg shadow-md">Hapus</button>
                                        </form>
                                    </li>
                                @endforeach
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript -->
    <script>
        document.getElementById('viewDetailsBtn').addEventListener('click', function () {
            document.getElementById('detailsSidebar').classList.remove('translate-x-full');
        });
    
        document.getElementById('closeSidebarBtn').addEventListener('click', function () {
            document.getElementById('detailsSidebar').classList.add('translate-x-full');
        });
    </script>

@include('footer')

<!-- SWEET ALERT -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<script>
    document.addEventListener('DOMContentLoaded', function () {
        @if(session('success'))
            Swal.fire({
                icon: 'success',
                title: 'Success',
                text: "{{ session('success') }}",
                confirmButtonText: 'OK',
                confirmButtonColor: '#3085d6'
            });
        @endif

        @if(session('error'))
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: "{{ session('error') }}",
                confirmButtonText: 'OK',
                confirmButtonColor: '#3085d6'
            });
        @endif
    });
</script>

<script>
document.addEventListener("DOMContentLoaded", () => {
    let selectedMKId = null;
    const searchInput = document.getElementById("search-input");
    const dropdown = document.getElementById("dropdown");
    const saveButton = document.getElementById("save-button");

    // Tampilkan dropdown saat input difokuskan
    searchInput.addEventListener("focus", () => {
        dropdown.classList.remove("hidden");
    });

    // Sembunyikan dropdown saat klik di luar
    document.addEventListener("click", (event) => {
        if (!dropdown.contains(event.target) && event.target.id !== "search-input") {
            dropdown.classList.add("hidden");
        }
    });

    // Filter hasil pencarian saat mengetik
    searchInput.addEventListener("input", () => {
        const searchValue = searchInput.value.toLowerCase();
        document.querySelectorAll(".add-mk").forEach((item) => {
            const text = item.textContent.toLowerCase();
            if (text.includes(searchValue)) {
                item.classList.remove("hidden");
            } else {
                item.classList.add("hidden");
            }
        });
    });

    // Saat klik item di dropdown
    document.querySelectorAll(".add-mk").forEach((item) => {
        item.addEventListener("click", (event) => {
            event.preventDefault();
            selectedMKId = item.getAttribute("data-id");
            const name = item.textContent.trim();
            // Masukkan teks ke input
            searchInput.value = name;
            // Sembunyikan dropdown
            dropdown.classList.add("hidden");
        });
    });

    // Saat tombol simpan ditekan, kirim data ke server
    saveButton.addEventListener("click", () => {
        if (!selectedMKId) {
            alert("Pilih mata kuliah terlebih dahulu.");
            return;
        }
        
        fetch("{{ route('irs.update') }}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": "{{ csrf_token() }}",
            },
            body: JSON.stringify({ 
                action: 'add',
                selectedMK: [{ id: selectedMKId }] 
            }),
        })
        .then((response) => {
            // Redirect akan dilakukan di server
            window.location.href = "{{ route('mahasiswa.irs_mhs') }}";
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    });

    // Tambahkan event listener untuk tombol hapus
    document.querySelectorAll('.remove-mk').forEach(button => {
        button.addEventListener('click', () => {
            const kode_mk = button.getAttribute('data-id');
            
            fetch("{{ route('irs.update') }}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-TOKEN": "{{ csrf_token() }}",
                },
                body: JSON.stringify({ 
                    action: 'remove',
                    selectedMK: [{ id: kode_mk }] 
                }),
            })
            .then((response) => {
                // Redirect akan dilakukan di server
                window.location.href = "{{ route('mahasiswa.irs_mhs') }}";
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        });
    });
});
</script>