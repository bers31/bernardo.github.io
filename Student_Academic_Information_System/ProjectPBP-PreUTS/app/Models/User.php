<?php

namespace App\Models;

// use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Str;


class User extends Authenticatable
{
    use HasFactory, Notifiable;
    protected static function boot()
    {
        parent::boot();

        static::creating(function ($user) {
            // Set the username to the part before the "@" in the email
            if (empty($user->username)) {
                $user->username = Str::before($user->email, '@');
            }
        });
    }
    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'email',
        'username',
        'password',
        'role',
    ];

    /**
     * The attributes that should be hidden for serialization.
     *
     * @var array<int, string>
     */
    protected $hidden = [
        'password',
        'remember_token',
    ];

    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
        ];
    }

    public function dosen()
    {
        return $this->hasOne(Dosen::class, 'email', 'email');
    }

    public function mahasiswa()
    {
        return $this->hasOne(Mahasiswa::class, 'email', 'email');
    }
    public function dekan(): HasOne
    {
        return $this->hasOne(Dekan::class, 'email', 'email'); // Sesuaikan kolom jika perlu
    }

    public function akademik(): HasOne
    {
        return $this->hasOne(Akademik::class, 'email', 'email');
    }

}
