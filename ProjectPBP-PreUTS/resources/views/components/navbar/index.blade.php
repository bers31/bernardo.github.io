<div class="flex items-center bg-[#DE2227] p-6">
  <!-- Logo and Dashboard Link -->
  <div class="text-white font-bold text-4xl pl-6">
    <a href="{{ route(Auth::user()->role . '.dashboard', 'dashboard') }}">SI-MAS</a>
  </div>

  <!-- Desktop Navbar Links -->
  <ul class="hidden lg:flex space-x-8 ml-20 text-white text-base pr-6 gap-14">
    @if(Auth::user()->role === "dosen")
      <x-navbar.list href="{{ route('dosen.perwalian') }}">Perwalian</x-navbar.list>
      <x-navbar.list href="{{ route('dosen.input_nilai') }}">Input Nilai</x-navbar.list>
    @endif

    @if(Auth::user()->role === "mahasiswa")
      <x-navbar.list href="{{ route('mahasiswa.status_akademik') }}">Status Akademik</x-navbar.list>
      <x-navbar.list href="{{ route('mahasiswa.irs_mhs') }}">IRS</x-navbar.list>
      <x-navbar.list href="{{ route('mahasiswa.khs_mhs') }}">KHS</x-navbar.list>
      <x-navbar.list href="{{ route('mahasiswa.transkrip_mhs') }}">Transkrip</x-navbar.list>
    @endif
  </ul>

  <!-- Mobile Navbar Links -->
  <div class="lg:hidden flex flex-col items-center justify-center space-y-4 mt-4 w-full text-white text-base">
    @if(Auth::user()->role === "mahasiswa")
      <x-navbar.m-list href="{{ route('mahasiswa.status_akademik') }}">Status Akademik</x-navbar.m-list>
      <x-navbar.m-list href="{{ route('mahasiswa.irs_mhs') }}">IRS</x-navbar.m-list>
      <x-navbar.m-list href="{{ route('mahasiswa.khs_mhs') }}">KHS</x-navbar.m-list>
      <x-navbar.m-list href="{{ route('mahasiswa.transkrip_mhs') }}">Transkrip</x-navbar.m-list>
    @endif

    @if(Auth::user()->role === "dosen")
      <x-navbar.m-list href="{{ route('dosen.perwalian') }}">Perwalian</x-navbar.m-list>
      <x-navbar.m-list href="{{ route('dosen.input_nilai') }}">Input Nilai</x-navbar.m-list>
    @endif

  </div>
</div>
