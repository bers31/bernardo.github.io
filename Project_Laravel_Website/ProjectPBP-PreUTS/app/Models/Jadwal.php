<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Jadwal extends Model
{
    use HasFactory;

    // Define the table name if it's not following Laravel's naming convention
    protected $table = 'jadwal';

    // Define the primary key
    protected $primaryKey = 'id_jadwal';

    // Mass-assignable attributes
    protected $fillable = [
        'id_jadwal',
        'status',
        'kode_mk',
        'jam_mulai',
        'jam_selesai',
        'kode_kelas',
        'ruang',
        'hari',
        'kuota',
        'kode_tahun',
    ];

    /**
     * Relationship with MataKuliah model.
     * Assumes that `kode_mk` in `jadwal` refers to `kode_mk` in `mata_kuliah`.
     */
    public function mataKuliah()
    {
        return $this->belongsTo(MataKuliah::class, 'kode_mk', 'kode_mk');
    }

    /**
     * Relationship with Ruang model.
     */

     public function detail_irs(){
        return $this->hasMany(DetailIRS::class, 'id_jadwal', 'id_jadwal');
     } 

    public function ruangan()
    {
        return $this->belongsTo(Ruang::class, 'ruang', 'kode_ruang');
    }

    public function detailIRS()
    {
        return $this->hasMany(DetailIRS::class, 'id_jadwal', 'id_jadwal');
    }

    public function dosen_pengampu()
    {
        return $this->hasMany(DosenPengampu::class, 'id_jadwal', 'id_jadwal');
    }
}
