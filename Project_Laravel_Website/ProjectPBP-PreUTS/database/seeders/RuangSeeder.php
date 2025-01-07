<?php

namespace Database\Seeders;

use App\Models\Ruang;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class RuangSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // DB::table('ruang')->insert([
        //     [
        //         'kode_ruang' => 'A102',
        //         'kode_departemen' => 'BIO',
        //     ],
        //     [
        //         'kode_ruang' => 'E101',
        //         'kode_departemen' => 'IF',
        //     ],
        //     [
        //         'kode_ruang' => 'E102',
        //         'kode_departemen' => 'IF',
        //     ],	
        // ]);
        Ruang::create(['kode_ruang'=>'E101','kode_departemen'=>'IF','kapasitas'=>'70']);
        Ruang::create(['kode_ruang'=>'E102','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'E103','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'A101','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'A102','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'A201','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'A204','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'A301','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'A302','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'A303','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'A202','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'B201','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'B103','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'K101','kode_departemen'=>'IF','kapasitas'=>'60']);
        Ruang::create(['kode_ruang'=>'K102','kode_departemen'=>'IF','kapasitas'=>'50']);
        Ruang::create(['kode_ruang'=>'K202','kode_departemen'=>'IF','kapasitas'=>'50']);
    }
}
